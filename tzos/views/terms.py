# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, abort, flash, g, render_template, redirect, \
    request, url_for

from flaskext.babel import gettext as _

from tzos.extensions import db, dbxml
from tzos.forms import AddTermForm, CommentForm, EditTermForm, ModEditTermForm
from tzos.models import Comment, Term
from tzos.helpers import dropdown_list, get_dict_langs, \
        get_origins_dropdown, get_responsible_orgs, require_valid_dict
from tzos.permissions import auth

terms = Module(__name__)

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

def generate_term_form(form_cls, **form_args):

    form = form_cls(**form_args)

    if form_cls.__name__ == 'AddTermForm':
        dict_langs = get_dict_langs()
        form.syntrans_lang.choices = dict_langs
        form.language.choices = dict_langs

    form.concept_origin.choices = get_origins_dropdown()

    form.normative_authorization_org.choices = \
        dropdown_list(get_responsible_orgs())

    return form

@terms.route('/add/')
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

    add_form = generate_term_form(AddTermForm, formdata=form_args)

    return render_template('terms/add.html', add_form=add_form)

@terms.route('/add/single/', methods=('POST',))
@auth.require(401)
def add_single():

    form = generate_term_form(AddTermForm)

    if form and form.validate_on_submit():
        term = Term()
        form.populate_obj(term)

        # Handle SelectMultipleFields
        term.subject_field = ";".join(form.subject_field.data)

        if term.insert():
            msg = _('Term added successfully. <a href="%(url)s">Go to the term</a>.',
                    url=url_for('terms.detail', id=term.id))
            flash(msg, 'success')
        else:
            flash(_('Error while trying to add the term.'), 'error')

        return redirect(url_for('terms.add'))

    return render_template('terms/add.html', add_form=form)

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

    form = generate_term_form(form_cls, obj=term)

    # BooleanField
    form.not_mine.data = not term.is_mine()

    if term.is_mine():
        form.originating_person.data = u""

    if form.validate_on_submit():
        # TODO: actual term updating
        success = []
        failure = []

        blacklist = ('not_mine', 'submit', 'administrative_status')

        for field in form:

            if field.type != 'HiddenField' and field.name not in blacklist:
                old_data = getattr(term, field.name)

                if field.data != old_data:
                    print field.data
                    print "We have to edit this"

                    if term.update(field.name, field.data):
                        success.append(field.name)
                    else:
                        failure.append(field.name)

        if failure:
            flash(_(u"Failed to edit some fields."), "error")
        else:
            flash(_(u"Term '%(term)s' has been edited.", term=term.term),
                    "success")

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

        flash(_("Thanks for your comment."), "success")

        return redirect(comment.url)

    return redirect(url_for("terms.detail", id=term_id))
