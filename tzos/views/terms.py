# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from time import strftime

from flask import Module, abort, flash, g, render_template, redirect, \
    request, url_for

from flaskext.babel import gettext as _

from tzos.extensions import db, dbxml
from tzos.forms import AddTermForm, CommentForm, EditTermForm, \
        ModEditTermForm, UploadForm
from tzos.models import Comment, Term
from tzos.helpers import get_dict_langs, get_origins_dropdown, \
        get_responsible_orgs, get_sfields_dropdown, require_valid_dict
from tzos.permissions import auth

terms = Module(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@terms.route('/<int:id>/')
def detail(id):

    qs = """
    import module namespace term = "http://tzos.net/term" at "term.xqm";

    let $tig := collection($collection)//tig[@id="{0}"]
    where term:owner($tig) = "{1}" or term:is_public($tig)
    return term:values($tig)
    """.format(unicode(id).encode('utf-8'),
               getattr(g.user, 'username', u'').encode('utf-8'))


    value = dbxml.session.raw_query(qs).as_str().first_or_404()
    term = Term.parse(value)

    comment_form = CommentForm(term_id=id)

    term_comments = Comment.query.filter(Comment.term_id==id).all()

    return render_template('terms/detail.html',
                           term=term,
                           comment_form=comment_form,
                           term_comments=term_comments)

def generate_term_form(form_cls, public_term=False, **form_args):

    form = form_cls(**form_args)

    if form_cls.__name__ == 'AddTermForm':
        dict_langs = get_dict_langs()
        form.syntrans_lang.choices = dict_langs
        form.language.choices = dict_langs
        form.eqlang.choices = dict_langs

    if form_cls.__name__ == 'ModEditTermForm':
        if public_term and not g.user.is_admin:
            form.working_status.choices = form.working_status.choices[2:]

    if form_cls.__name__ == 'UploadForm':
        dict_langs = get_dict_langs()

        term_choices = [(u'term-' + code, lang) for code, lang in dict_langs]
        form.term_field.choices = term_choices

        other_choices = [(u'trans-' + code,
            _(u"Synonym/translation in %(lang)s", lang=lang)) \
            for code, lang in dict_langs]
        form.other_fields.choices = other_choices

    form.concept_origin.choices = get_origins_dropdown()
    form.subject_field.choices = get_sfields_dropdown(g.ui_lang)

    if hasattr(form, 'normative_authorization_org'):
        form.normative_authorization_org.choices = get_responsible_orgs()

    return form


def _do_the_insert(term):

    results = []

    if term.exists():
        msg = _(u"Term ‘%(term)s’ already exists.",
                term=term.term)
        results.append((msg, 'warning'))
    else:
        if term.insert():
            msg = _(u"Term ‘%(term)s’ added successfully.",
                    term=term.term)
            results.append((msg, 'success'))
        else:
            msg = _(u"Error while adding term ‘%(term)s’.",
                    term=term.term)
            results.append((msg, 'error'))

    return results


@terms.route('/add/', methods=('GET', 'POST'))
@auth.require(401)
def add():

    form_args = None

    if request.args and 'term' in request.args and 'lang' in request.args:
        form_args = request.args.copy()

        form_args['add-syntrans_term'] = request.args['term']
        form_args['add-syntrans_lang'] = request.args['lang']
        form_args['add-syntrans'] = True

        del form_args['term']
        del form_args['lang']

    add_form = generate_term_form(AddTermForm, formdata=form_args,
                                  prefix='add')
    upload_form = generate_term_form(UploadForm, formdata=form_args,
                                     prefix='upload')

    if add_form.submit.data and add_form.validate_on_submit():

        term = Term()
        add_form.populate_obj(term)

        if term.insert():
            msg = _(u'Term added successfully. '
                    '<a href="%(url)s">Go to the term</a>.',
                    url=url_for('terms.detail', id=term.id))
            flash(msg, 'success')

            return redirect(url_for("terms.add"))
        else:
            flash(_(u'Error while trying to add the term.'), 'error')

    elif upload_form.submit.data and upload_form.validate_on_submit():
        file = request.files['upload-file']

        fields = upload_form.columns.data.split(u";")
        fields.insert(0, upload_form.term_field.data)

        if file and allowed_file(file.filename):
            import csv

            reader = csv.DictReader(file, fieldnames=fields, skipinitialspace=True)

            results = []

            for row in reader:

                # Store current term for using as a reference for
                # synonyms and translations
                try:
                    # TODO: clean the input before blindly insert it
                    current_term = unicode(row[fields[0]], 'utf-8').strip()
                    current_language = fields[0][5:7]
                except IndexError:
                    current_term = None
                    current_language = None

                for field in fields:

                    term = Term()
                    upload_form.populate_obj(term)

                    if term.working_status == u'starterElement':
                        term.working_status = u'importedElement'

                    if not row[field]:
                        continue

                    value = unicode(row[field], 'utf-8').strip()

                    if not value:
                        # No value passed, skip this field
                        continue

                    if field.startswith('term-'):

                        # Fill in fields
                        term.term = value
                        term.language = field[5:7]

                        results += _do_the_insert(term)

                    elif field.startswith('trans-'):

                        # Fill in fields
                        term.term = value
                        term.language = field[6:8]
                        term.syntrans = True
                        term.syntrans_term = current_term
                        term.syntrans_language = current_language

                        results += _do_the_insert(term)

            return render_template('terms/upload_results.html', results=results)
        else:
            flash(_(u'Not a valid file.'), 'error')

    return render_template('terms/add.html', add_form=add_form,
                                             upload_form=upload_form)

@terms.route('/<int:id>/edit/', methods=('GET', 'POST'))
@auth.require(401)
def edit(id):

    term = Term(id)
    term.populate()

    # BooleanFields
    if not g.user.is_moderator:
        term.working_status = term.is_public()

    if g.user.is_moderator:
        form_cls = ModEditTermForm
    else:
        form_cls = EditTermForm

    form = generate_term_form(form_cls, term.is_public(), obj=term)

    if form.validate_on_submit():
        success = []
        failure = []

        blacklist = ('not_mine', 'submit',
                     'cross_reference', 'normative_authorization',
                     'normative_authorization_org')

        for field in form:

            if field.type != 'HiddenField' and field.name not in blacklist:
                old_data = getattr(term, field.name)
                new_data = field.data

                if new_data != old_data:

                    if term.update(field.name, new_data):
                        success.append(field.name)
                    else:
                        failure.append(field.name)

        #
        # Treat excepcional cases (xref, normative_auth)
        #

        if form.cross_reference.data != term.cross_reference:
            xref_term = Term(term=form.cross_reference.data)
            xref_id = xref_term.id

            olds = (u'//tig[@id="{0}"]/ref[@type="crossReference"]', u'//tig[@id="{0}"]/../../ref[@type="crossReference"]')

            new = u'<ref target="{0}" type="crossReference">{1}</ref>'. \
                    format(xref_id, form.cross_reference.data)

            for old in olds:
                old = old.format(term.id)

                if dbxml.session.replace(old, new):
                    success.append(field.name)
                else:
                    failure.append(field.name)

        if form.normative_authorization.data != \
           term.normative_authorization or \
           form.normative_authorization_org.data != \
           term.normative_authorization_org:

            old = u'//tig[@id="{0}"]/termNote[@type="normativeAuthorization"]'. \
                format(term.id)
            new = u'<termNote type="normativeAuthorization" '\
                  'target="{0}">{1}</termNote>'. \
                format(form.normative_authorization_org.data,
                       form.normative_authorization.data)

            if dbxml.session.replace(old, new):
                success.append(field.name)
            else:
                failure.append(field.name)

        if failure:
            flash(_(u"Failed to edit some fields."), "error")
        else:
            # XXX: adapt 'modification'? add note?
            ctx = {
                'transac_type': 'modification',
                'date': strftime('%Y-%m-%d %H:%M:%S%z'),
                'username': g.user.username
            }

            xml = render_template('xml/transaction.xml', **ctx)

            locations = (u'//tig[@id="{0}"]',
                         u'//tig[@id="{0}"]/../..')

            for location in locations:
                location = location.format(id)
                dbxml.session.insert_as_last(xml, location)

            flash(_(u"Term ‘%(term)s’ has been edited.", term=term.term),
                    "success")

            return redirect(url_for("terms.edit", id=id))

    elif request.method == 'POST' and not form.validate():
        flash(_(u"Failed to edit term. Please review the data you "
                 "entered is correct."), "error")

    return render_template('terms/edit.html', form=form, term=term)

@terms.route("/<int:term_id>/comment/", methods=("POST",))
@auth.require(401)
def add_comment(term_id):

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(author=g.user)

        form.populate_obj(comment)

        db.session.add(comment)
        db.session.commit()

        flash(_(u"Thanks for your comment."), "success")

        return redirect(comment.url)

    return redirect(url_for("terms.detail", id=term_id))
