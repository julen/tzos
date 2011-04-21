# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, render_template, redirect, url_for

from flaskext.babel import gettext as _

from tzos.extensions import dbxml
from tzos.forms import AddTermForm
from tzos.models import Term
from tzos.helpers import get_dict_langs, get_working_statuses, \
    require_valid_dict

terms = Module(__name__)

@terms.route('/<id>/')
def detail(id):

    ctx = {'id': id}
    rendered_term = dbxml.get_db().template_query('terms/xq_term_detail.html',
                                                  context=ctx) \
                                  .as_rendered().first()

    return render_template('terms/term_detail.html',
                           rendered_term=rendered_term)

def generate_add_term_form():
    form = AddTermForm()

    form.language.choices = get_dict_langs()
    form.syntrans_lang.choices = get_dict_langs()

    return form

@terms.route('/add/')
def add():
    add_term_form = generate_add_term_form()

    return render_template('terms/add.html', add_term_form=add_term_form)

@terms.route('/add/single/', methods=('POST',))
def add_single():
    form = generate_add_term_form()

    if form and form.validate_on_submit():
        term = Term()
        form.populate_obj(term)

        if term.insert():
            msg = _('Term added successfully. <a href="%(url)s">Go to the term</a>.',
                    url=url_for('terms.detail', id=term.id))
            flash(msg, 'success')
        else:
            flash(_('Error while trying to add the term.'), 'error')

    return redirect(url_for('terms.add'))
