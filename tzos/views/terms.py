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
from tzos.helpers import require_valid_dict

terms = Module(__name__)

@terms.route('/<id>/')
def detail(id):

    ctx = {'id': id}
    term = dbxml.get_db().template_query('terms/xq_term_detail.html',
                                         context=ctx).as_rendered().first()

    return render_template('terms/term_detail.html', term=term)

@terms.route('/add/')
def add():
    return "Foo"
