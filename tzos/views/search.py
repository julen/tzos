# -*- coding: utf-8 -*-
"""
    tzos.views.search
    ~~~~~~~~~~~~~~~~~

    Search views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, g, render_template, request, redirect, url_for

from flaskext.babel import lazy_gettext as _

from tzos.extensions import dbxml
from tzos.forms import SearchForm
from tzos.helpers import dropdown_list, get_dict_langs

search = Module(__name__)

@search.route('/')
def quick():
    q = request.args.get('q', '').strip()

    if not q:
        return redirect(url_for('search.advanced'))

    pn = int(request.args.get('p', 1))
    ctx = {'q': q}

    page = dbxml.get_db().template_query('search/results.xq',
                                         context=ctx).as_rendered(). \
                                         paginate(pn, 10, error_out=False)

    return render_template('search/results.html', q=q, page=page)

@search.route('/advanced/', methods=('GET', 'POST',))
def advanced():
    page = None
    form = SearchForm()

    form.language.choices = dropdown_list(get_dict_langs(), 'all', _('All'))

    if form.validate_on_submit():
        pn = int(request.args.get('p', 1))
        ctx = {'q': form.keywords.data}

        page = dbxml.get_db().template_query('search/results.xq',
                                             context=ctx).as_rendered(). \
                                             paginate(pn, 10, error_out=False)

    return render_template('search/advanced.html', form=form, page=page)
