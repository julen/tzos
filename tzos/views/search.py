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

def _get_search_param(key):
    val = request.args.get(key, '')

    if val and val == 'all':
        val = ''

    return val

def _get_search_filters():

    filter = "true() "

    lang = _get_search_param('lang')

    if lang:
        filter += 'and $term/../..[@xml:lang="{0}"]'.format(lang)

    return filter

@search.route('/')
def quick():
    page = None
    q = request.args.get('q', '').strip()

    if q:
        pn = int(request.args.get('p', 1))

        filter = _get_search_filters()
        print filter
        #ctx = {'q': q, 'filter': _get_search_filters() }

        qs = """
        import module namespace term = "http://tzos.net/term" at "term.xqm";

        for $term in collection($collection)//term
        where dbxml:contains($term/string(), "{0}") and
              term:is_public($term) and {1}
        return term:asLink($term)
        """.format(q, filter)
        print qs

        page = dbxml.get_db().raw_query(qs).as_str(). \
                                            paginate(pn, 10, error_out=False)

    form = SearchForm(request.args, csrf_enabled=False)

    form.lang.choices = dropdown_list(get_dict_langs(), 'all', _('All'))

    return render_template('search/results.html', form=form, q=q, page=page)
