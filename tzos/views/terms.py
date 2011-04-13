# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, render_template

from tzos.extensions import dbxml
from tzos.forms import AddTermForm
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

@terms.route('/add/')
def add():
    form = AddTermForm()
    # TODO: Get a list of available languages form the XCS file
    form.language.choices = get_dict_langs()

    form.element_working_status.choices = get_working_statuses()

    return render_template('terms/add.html', form=form)
