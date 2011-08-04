# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from operator import itemgetter
from time import strftime

from flask import Module, abort, current_app, flash, g, render_template, \
        redirect, request, url_for

from flaskext.babel import gettext as _, lazy_gettext as _l
from flaskext.wtf import TextField

from tzos.extensions import db, dbxml
from tzos.forms import AddTermForm, AddTermFormCor, CommentForm, \
        CollisionForm, CollisionFormCor, EditTermForm, EditTermFormCor, \
        EditTermFormMod, UploadForm, UploadFormCor
from tzos.models import Comment, Term, TermUpload
from tzos.helpers import get_dict_langs, get_origins_dropdown, \
        get_responsible_orgs, get_sfields_dropdown, require_valid_dict
from tzos.permissions import auth, corrector

terms = Module(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def _register_transaction(id, type='modification'):
    """Writes transaction information for the tig with id `id`."""

    ctx = {
        'transac_type': type,
        'date': strftime('%Y-%m-%d %H:%M:%S%z'),
        'username': g.user.username
    }

    xml = render_template('xml/transaction.xml', **ctx)

    locations = (u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]',
                 u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../..')

    for location in locations:
        location = location.format(id)
        dbxml.session.insert_as_last(xml, location)


@terms.route('/<int:id>/')
def detail(id):

    qs = """
    import module namespace term = "http://tzos.net/term" at "term.xqm";

    let $tig := collection($collection)/martif/text/body/termEntry/langSet/tig[@id="{0}"]
    let $unreviewed :=
        if (term:owner($tig) = "{1}") then
            true()
        else
            false()
    where term:owner($tig) = "{1}" or term:is_public($tig)
    return term:values($tig, $unreviewed)
    """.format(unicode(id).encode('utf-8'),
               getattr(g.user, 'username', u'').encode('utf-8'))


    term = dbxml.session.raw_query(qs).as_callback(Term.parse).first_or_404()

    comment_form = CommentForm(term_id=id)

    term_comments = Comment.query.filter(Comment.term_id==id).all()

    return render_template('terms/detail.html',
                           term=term,
                           comment_form=comment_form,
                           term_comments=term_comments)

def _gen_term_form(form_cls, **form_args):

    if form_cls.__name__ in ('AddTermForm', 'AddTermFormCor', \
            'CollisionForm', 'CollisionFormCor'):

        dict_langs = get_dict_langs()

        # Hack for dynamically generating form fields
        class F(form_cls):
            pass

        eqterm_desc = _(u"Separate terms using commas.")

        for code, name in dict_langs:
            field_name = 'eqterm-{0}'.format(code)
            field_label = _l(u'Equivalents — %(lang)s', lang=name)
            # TODO: validate for clear input
            setattr(F, field_name, TextField(field_label,
                                             description=eqterm_desc))

        form = F(**form_args)

        form.syntrans_lang.choices = dict_langs
        form.language.choices = dict_langs
        form.eqlang.choices = dict_langs

    elif form_cls.__name__ in ('UploadForm', 'UploadFormCor'):

        form = form_cls(**form_args)

        dict_langs = get_dict_langs()

        term_choices = [(u'term-' + code, lang) for code, lang in dict_langs]
        form.term_field.choices = term_choices

        other_choices = [(u'trans-' + code,
            _(u"Equivalent in %(lang)s", lang=lang)) \
            for code, lang in dict_langs]
        form.other_fields.choices = other_choices

    else:

        form = form_cls(**form_args)

        # Avoid explicit editing of Basque terms in certain situations
        if (not g.user.is_corrector and form.language.data == u'eu'):
            del form.term

    form.concept_origin.choices = get_origins_dropdown()
    form.subject_field.choices = get_sfields_dropdown(g.ui_lang)

    if hasattr(form, 'normative_authorization_org'):
        form.normative_authorization_org.choices = get_responsible_orgs()

    return form


def _populate_equivalents(form, term):
    """Populates `term` equivalents that have been submitted in the `form`."""

    for field in form:
        if u'eqterm-' in field.name:
            lang = field.name.rsplit(u'-', 1)[1]
            terms = field.data

            if terms:
                terms = terms.split(u',')

                if lang == term.language:
                    term.append_raw_synonym(terms)
                else:
                    term.append_raw_translation(lang, terms)


@terms.route('/add/', methods=('GET', 'POST'))
@auth.require(401)
def add():

    form_args = None

    if request.args and 'term' in request.args and 'lang' in request.args:
        form_args = request.args.copy()

        form_args['add-syntrans_term'] = request.args['term']
        form_args['add-syntrans_lang'] = request.args['lang']
        form_args['add-syntrans'] = True
        form_args['collision-syntrans_term'] = request.args['term']
        form_args['collision-syntrans_lang'] = request.args['lang']
        form_args['collision-syntrans'] = True

        del form_args['term']
        del form_args['lang']

    if g.user.is_corrector:
        add_form_cls = AddTermFormCor
        upload_form_cls = UploadFormCor
        collision_form_cls = CollisionFormCor
    else:
        add_form_cls = AddTermForm
        upload_form_cls = UploadForm
        collision_form_cls = CollisionForm

    add_form = _gen_term_form(add_form_cls, formdata=form_args,
                                  prefix='add')
    collision_form = _gen_term_form(collision_form_cls, formdata=form_args,
                                  prefix='collision', csrf_enabled=False)
    upload_form = _gen_term_form(upload_form_cls, formdata=form_args,
                                     prefix='upload', csrf_enabled=False)

    if (add_form.submit.data and add_form.validate_on_submit()) or \
        ((collision_form.discard.data or collision_form.force.data) and \
        collision_form.validate_on_submit()):

        # Get desired extra action (only used in collision pages)
        force = False
        discard = False
        if collision_form.discard.data:
            discard = True
        elif collision_form.force.data:
            force = True

        if discard:
            flash(_(u"Term addition discarded."), 'success')
            return redirect(url_for('frontend.index'))

        term = Term()
        if collision_form.force.data:
            collision_form.populate_obj(term)
        else:
            add_form.populate_obj(term)

        _populate_equivalents(add_form, term)

        st, results, objects = term.insert_all(force=force)

        if st == u"success":
            msg = _(u'Term added successfully. '
                    '<a href="%(url)s">Go to the term</a>.',
                    url=url_for('terms.detail', id=term.id))
            flash(msg, 'success')

            return redirect(url_for("terms.add"))
        elif st == u"collision":
            msg = _(u'Collision detected!')
            flash(msg, 'warning')

            # Fill in collision form
            for field in add_form:
                if field.name != 'csrf':
                    setattr(collision_form, field.name, field.data)

            return render_template('terms/collision.html',
                    add_form=add_form,
                    collision_form=collision_form,
                    terms=objects)
        else:
            flash(_(u'Error while trying to add some terms.'), 'error')

    elif (upload_form.submit.data or upload_form.confirm.data or \
          upload_form.cancel.data) and upload_form.validate_on_submit():

        if upload_form.cancel.data:
            flash(_(u"Import action cancelled."), 'success')
            return redirect(url_for('frontend.index'))

        emulate = True
        if upload_form.confirm.data:
            emulate = False

        # Save for later reuse
        disk_fn = None
        if emulate:
            import os
            import random
            import string
            import tempfile

            f = request.files['upload-file']
            fn = ''.join(random.choice(string.lowercase) for x in range(6))
            disk_fn = os.path.join(tempfile.gettempdir(), fn)
            f.save(disk_fn)
            upload_form.fpath.data = disk_fn

        try:
            file = open(upload_form.fpath.data)
        except IOError:
            file = None

        fields = upload_form.columns.data.split(u";")
        fields.insert(0, upload_form.term_field.data)

        if file:
            import csv

            reader = csv.DictReader(file, fieldnames=fields, skipinitialspace=True)

            results = {}

            if not emulate:
                term_upload = TermUpload(author=g.user)

            for (count, row) in enumerate(reader):

                # Break on the max num. of allowed term uploads
                if count == current_app.config.get('TZOS_MAX_UPLOADS', 100):
                    break

                # Store current term for using as a reference for
                # synonyms and translations
                try:
                    # TODO: clean the input before blindly insert it
                    current_term = unicode(row[fields[0]], 'utf-8').strip()
                    current_language = fields[0][5:7]
                except IndexError:
                    current_term = None
                    current_language = None

                term = Term()
                upload_form.populate_obj(term)

                if term.working_status == u'starterElement':
                    term.working_status = u'importedElement'

                for field in fields:

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

                    elif field.startswith('trans-'):

                        lang = field[6:8]

                        if term.language == lang:
                            term.append_raw_synonym(value)
                        else:
                            term.append_raw_translation(lang, value)

                st, res, objects = term.insert_all(emulate=emulate)
                results.setdefault(st, []).append(res)

                # Add resulting terms to the upload tracking structure
                if not emulate:
                    for (term, status) in res:
                        if status == u'success':
                            term_upload.add(term)

            # Once all is processed, save the upload tracking structure
            if not emulate:
                db.session.add(term_upload)
                db.session.commit()

            # We need to set this again due to the postprocessing
            upload_form.fpath.data = disk_fn

            return render_template('terms/upload_results.html',
                    results=results,
                    upload_form=upload_form,
                    emulate=emulate)
        else:
            flash(_(u'Not a valid file.'), 'error')

    return render_template('terms/add.html', add_form=add_form,
                                             upload_form=upload_form)

@terms.route('/<int:id>/edit/', methods=('GET', 'POST'))
@auth.require(401)
def edit(id):

    if g.user.is_corrector:
        user_restriction = "true()"
    else:
        user_restriction = "term:is_public($tig)"

    qs = """
    import module namespace term = "http://tzos.net/term" at "term.xqm";

    let $tig := collection($collection)/martif/text/body/termEntry/langSet/tig[@id="{0}"]
    let $unreviewed :=
        if (term:owner($tig) = "{1}") then
            true()
        else
            false()
    where term:owner($tig) = "{1}" or {2}
    return term:values($tig, $unreviewed)
    """.format(unicode(id).encode('utf-8'),
               getattr(g.user, 'username', u'').encode('utf-8'),
               user_restriction)

    term = dbxml.session.raw_query(qs).as_callback(Term.parse).first_or_404()

    try:
        term.lock()
    except Term.TermLocked:
        return render_template('terms/locked.html')

    # Be aware these checks have to be done from highest to lowest permissions
    if g.user.is_moderator:
        form_cls = EditTermFormMod
    elif g.user.is_corrector:
        form_cls = EditTermFormCor
    else:
        form_cls = EditTermForm

    form = _gen_term_form(form_cls, obj=term)

    #
    # Adapt working_status for reviewing cases
    #
    review = request.args.get('mode', u'') == u'review'

    if g.user.is_moderator and review:
        form.working_status.data = u"workingElement"
    elif g.user.is_corrector and review:
        form.working_status.data = True
    elif not g.user.is_moderator and g.user.is_corrector:
        form.working_status.data = term.is_public

    if form.validate_on_submit():
        success = []
        failure = []

        blacklist = ('not_mine', 'submit', 'normative_authorization',
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
        # Treat excepcional cases (ormative_authorization)
        #

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
            _register_transaction(id)

            term.unlock()

            flash(_(u"Term ‘%(term)s’ has been edited.", term=term.term),
                    "success")

            return redirect(url_for("terms.detail", id=id))

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


@terms.route('/review/')
@corrector.require(401)
def review_ui():

    qs = """
    import module namespace term = "http://tzos.net/term" at "term.xqm";

    for $tig in collection($collection)/martif/text/body/termEntry/langSet/tig
    where term:is_unreviewed($tig)
    order by term:sortkey($tig) ascending, term:term($tig) ascending
    return term:values($tig, true())
    """

    terms = dbxml.session.raw_query(qs).as_callback(Term.parse).all()

    return render_template('terms/review.html', terms=terms)


@terms.route('/<int:id>/review/<any(accept, reject):action>/')
@corrector.require(401)
def review(id, action):

    action_map = {
            'accept': 'workingElement',
            'reject': 'archiveElement',
            }

    qs = 'replace value of node collection($collection)/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="elementWorkingStatus"] with "{1}"'
    qs = qs.format(id, action_map[action])

    if dbxml.session.insert_raw(qs):

        if action == 'accept':
            _register_transaction(id)
            flash(_(u"Term accepted."), "success")
        else:
            _register_transaction(id, type='withdrawal')
            flash(_(u"Term rejected."), "success")
    else:
        flash(_(u"Failed to perform action."), "error")

    return redirect(url_for("terms.review_ui"))
