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

terms = Module(__name__)

@terms.route('/')
def list_all():
    qs = '/martif/text/body/termEntry/langSet[@xml:lang="%s"]/tig/term/string()' % (session['tzos_dict'])
    terms = dbxml.get_db().query(qs).as_str().all()

    return render_template('terms/list_all.html', terms=terms)

@terms.route('/<string(length=1):letter>/')
def list_letter(letter):

    ctx = {'lang': session['tzos_dict'], 'letter': letter}
    terms = dbxml.get_db().template_query('terms/xquery_term.html',
                                          context=ctx).as_rendered().all()

    return render_template('terms/list_letter.html', terms=terms, letter=letter)
