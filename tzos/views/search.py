# -*- coding: utf-8 -*-
"""
    tzos.views.search
    ~~~~~~~~~~~~~~~~~

    Search views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, g, render_template, request

from tzos.helpers import url_for

search = Module(__name__)

@search.route('/')
def quick():
    q = request.args.get('q', '').strip()

    if not q:
        return render_template('search/advanced.html')

    qs = '/martif/text/body/termEntry/langSet/tig/term[contains(string(), "%s")]/string()' % (q)
    terms = g.dbxml.query(qs).as_str().all()

    return render_template('search/results.html', q=q, results=terms)