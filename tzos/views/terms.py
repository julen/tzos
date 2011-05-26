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
from tzos.helpers import dropdown_list, get_dict_langs, \
        get_origins_dropdown, get_responsible_orgs, require_valid_dict
from tzos.permissions import auth
from tzos.strings import *

terms = Module(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@terms.route('/<int:id>/')
def detail(id):

    ctx = { 'id': id, 'current_user': getattr(g.user, 'username', '') }
    rendered_term = dbxml.get_db().template_query('terms/term_detail.xq',
                                                  context=ctx) \
                                  .as_rendered().first_or_404()

    comment_form = CommentForm(term_id=id)

    term_comments = Comment.query.filter(Comment.term_id==id).all()

    return render_template('terms/term_detail.html',
                           rendered_term=rendered_term,
                           comment_form=comment_form,
                           term_id=id,
                           term_comments=term_comments)

def generate_term_form(form_cls, public_term=False, **form_args):

    form = form_cls(**form_args)

    if form_cls.__name__ == 'AddTermForm':
        dict_langs = get_dict_langs()
        form.syntrans_lang.choices = dict_langs
        form.language.choices = dict_langs

    if form_cls.__name__ == 'ModEditTermForm':
        if public_term and not g.user.is_admin:
            form.working_status.choices = form.working_status.choices[2:]

    form.concept_origin.choices = get_origins_dropdown()
    form.subject_field.choices = sorted(SUBJECT_FIELDS, key=lambda x: x[1])

    if hasattr(form, 'normative_authorization_org'):
        form.normative_authorization_org.choices = \
            dropdown_list(get_responsible_orgs())

    return form

@terms.route('/add/', methods=('GET', 'POST'))
@auth.require(401)
def add():

    form_args = None

    if request.args and 'term' in request.args and 'lang' in request.args:
        form_args = request.args.copy()

        form_args['syntrans_term'] = request.args['term']
        form_args['syntrans_lang'] = request.args['lang']
        form_args['syntrans'] = True

        del form_args['term']
        del form_args['lang']

    add_form = generate_term_form(AddTermForm, formdata=form_args,
                                  prefix='add')
    upload_form = generate_term_form(UploadForm, formdata=form_args,
                                     prefix='upload')

    if add_form.submit.data and add_form.validate_on_submit():

        term = Term()
        add_form.populate_obj(term)

        # Handle SelectMultipleFields
        term.subject_field = ";".join(add_form.subject_field.data)

        if term.insert():
            msg = _('Term added successfully. <a href="%(url)s">Go to the term</a>.',
                    url=url_for('terms.detail', id=term.id))
            flash(msg, 'success')
        else:
            flash(_('Error while trying to add the term.'), 'error')

    elif upload_form.submit.data and upload_form.validate_on_submit():
        file = request.files['upload-file']

        if file and allowed_file(file.filename):
            pass
            # TODO: upload logic
        else:
            flash(_('Not a valid file.'), 'error')

    return render_template('terms/add.html', add_form=add_form,
                                             upload_form=upload_form)

@terms.route('/<int:id>/edit/', methods=('GET', 'POST'))
@auth.require(401)
def edit(id):

    if not g.user.owns_term(id) and \
       not g.user.is_moderator and \
       not g.user.is_admin:
        abort(403)

    term = Term(id)
    term.populate()

    # Handle SelectMultipleFields
    term.subject_field = term.subject_field.split(';')

    # BooleanFields
    if not g.user.is_moderator:
        term.working_status = term.is_public()

    if g.user.is_moderator:
        form_cls = ModEditTermForm
    else:
        form_cls = EditTermForm

    form = generate_term_form(form_cls, term.is_public(), obj=term, prefix='edit')

    if form.validate_on_submit():
        success = []
        failure = []

        blacklist = ('not_mine', 'submit',
                     'cross_reference', 'normative_authorization',
                     'normative_authorization_org')

        # Handle SelectMultipleFields
        form.subject_field.data = ";".join(form.subject_field.data)

        for field in form:

            if field.type != 'HiddenField' and field.name not in blacklist:
                old_data = getattr(term, field.name)
                if field.type in ('DynamicSelectField', 'SelectField') \
                and field.data == 'none':
                    new_data = ''
                else:
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

            olds = ('//term[@id="{0}"]/../ref[@type="crossReference"]', '//term[@id="{0}"]/../../../ref[@type="crossReference"]')

            new = '<ref target="{0}" type="crossReference">{1}</ref>'. \
                    format(xref_id, form.cross_reference.data)

            for old in olds:
                old = old.format(term.id)

                if dbxml.get_db().replace(old, new):
                    success.append(field.name)
                else:
                    failure.append(field.name)

        if form.normative_authorization.data != \
           term.normative_authorization or \
           form.normative_authorization_org.data != \
           term.normative_authorization_org:

            old = '//term[@id="{0}"]/../termNote[@type="normativeAuthorization"]'. \
                format(term.id)
            new = '<termNote type="normativeAuthorization" '\
                  'target="{0}">{1}</termNote>'. \
                format(form.normative_authorization_org.data,
                       form.normative_authorization.data)

            if dbxml.get_db().replace(old, new):
                success.append(field.name)
            else:
                failure.append(field.name)

        if failure:
            flash(_(u"Failed to edit some fields."), "error")
        else:
            # XXX: adapt 'modification'? add note?
            ctx = {
                'transac_type': 'modification',
                'date': strftime('%Y-%m-%d'),
                'username': g.user.username
            }

            xml = render_template('xml/transaction.xml', **ctx)

            locations = ('//term[@id="{0}"]/..',
                         '//term[@id="{0}"]/../../..')

            for location in locations:
                location = location.format(id)
                dbxml.get_db().insert_as_last(xml, location)

            flash(_(u"Term ‘%(term)s’ has been edited.", term=term.term),
                    "success")

    elif request.method == 'POST' and not form.validate():
        flash(_(u"Failed to edit term. Please review the data you "
                 "entered is correct."), "error")

    # BooleanField
    if term.is_mine():
        form.originating_person.data = u""

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

        flash(_("Thanks for your comment."), "success")

        return redirect(comment.url)

    return redirect(url_for("terms.detail", id=term_id))
