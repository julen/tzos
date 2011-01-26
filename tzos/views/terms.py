# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, g, render_template

from flaskext.babel import gettext as _

from tzos.extensions import dbxml

terms = Module(__name__)

@terms.route('/')
def list_all():
    terms_list = []

    qs = 'collection()/martif/text/body/termEntry/langSet[@xml:lang="%s"]/tig/term/string()' % (g.dict)
    terms = dbxml.query(qs)
    #terms = dbxml.query("distinct-values(collection()/martif/text/body/termEntry/langSet/@xml:lang)")

    while terms.hasNext():
        cur = terms.next()
        terms_list.append(cur.asString().decode('utf-8'))

    return render_template('terms/list_all.html', terms=terms_list)

@terms.route('/0-9/')
@terms.route('/<string(length=1):letter>/')
def list_letter(letter='0-9'):
    letter = str(letter)
    terms_list = []

    qs = 'collection()/martif/text/body/termEntry/langSet[@xml:lang="%s"]/tig/term[starts-with(string(), "%s")]/string()' % (g.dict, letter)
    terms = dbxml.query(qs)

    while terms.hasNext():
        cur = terms.next()
        terms_list.append(cur.asString().decode('utf-8'))

    return render_template('terms/list_letter.html', terms=terms_list,
                                                     letter=letter)
