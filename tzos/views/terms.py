# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, render_template, url_for

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

@terms.route('/add/', methods=('GET', 'POST'))
def add():
    form = AddTermForm()

    # TODO: Get a list of available languages form the XCS file
    form.language.choices = get_dict_langs()
    form.syntrans_lang.choices = get_dict_langs()

    form.element_working_status.choices = get_working_statuses()

    if form and form.validate_on_submit():
        term = Term()
        form.populate_obj(term)

        if term.insert():
            msg = _('Term added successfully. <a href="%(url)s">Go to the term</a>.',
                    url=url_for('terms.detail', id=term.id))
            flash(msg, 'success')
        else:
            flash(_('Error while trying to add the term.'), 'error')

    return render_template('terms/add.html', form=form)
