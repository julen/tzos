# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, g, render_template, session

from flaskext.babel import gettext as _

from tzos.extensions import dbxml

glossary = Module(__name__)

@glossary.route('/<dict>/<string(length=1):letter>/')
def list_letter(dict, letter):

    ctx = {'lang': dict, 'letter': letter}
    terms = dbxml.get_db().template_query('glossary/xquery_term.html',
                                          context=ctx).as_rendered().all()

    return render_template('glossary/list_letter.html', terms=terms, letter=letter)
