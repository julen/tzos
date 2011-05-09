# -*- coding: utf-8 -*-
"""
    tzos.views.search
    ~~~~~~~~~~~~~~~~~

    Search views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, g, render_template, request, url_for

from tzos.extensions import dbxml
from tzos.forms import SearchForm

search = Module(__name__)

@search.route('/')
def quick():
    q = request.args.get('q', '').strip()

    if not q:
        form = SearchForm()
        return render_template('search/advanced.html', form=form)

    pn = int(request.args.get('p', 1))
    ctx = {'q': q}

    page = dbxml.get_db().template_query('search/results.xq',
                                         context=ctx).as_rendered(). \
                                         paginate(pn, 10, error_out=False)

    return render_template('search/results.html', q=q, page=page)
