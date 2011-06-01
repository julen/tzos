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
from tzos.helpers import dropdown_list, get_dict_langs, \
        get_origins_dropdown, get_responsible_orgs, get_terms_from_values
from tzos.pagination import paginate
from tzos.strings import *

search = Module(__name__)

def _get_search_param(key):
    val = request.args.get(key, '')

    if val and (val == 'all'):
        val = ''

    return val

def _get_search_predicate(q):
    default_field = 'term'
    search_func = 'dbxml:contains'

    predicates = {
        'term': 'term:term($tig)',
        'definition': 'term:definition($tig)',
        'context': 'term:context($tig)',
        'example': 'term:example($tig)',
        'explanation': 'term:explanation($tig)',
        'hyponym': 'term:subordinate_cg($tig)',
        'hypernym': 'term:superordinate_cg($tig)',
        'antonym': 'term:antonym_concept($tig)',
        'related': 'term:related_concept($tig)',
    }

    field = _get_search_param('field')

    if not field:
        field = default_field

    try:
        predicate = predicates[field]
    except KeyError:
        predicate = predicates[default_field]

    return u'{0}({1}, "{2}")'.format(search_func, predicate, q)

def _get_search_filters():

    f_str = ""

    filters = (
        ('lang', '$tig/..[@xml:lang="{0}"]'),
        ('subject_field', '(let $fields := tokenize(term:subject_field($tig), ";") return some $f in $fields satisfies $f = "{0}")'),
        ('product_subset', 'term:product_subset($tig) = "{0}"'),
        ('concept_origin', 'term:concept_origin($tig) = "{0}"'),
        ('na', 'term:norm_auth($tig) = "{0}"'),
        ('na_org', '$tig/termNote[@type="normativeAuthorization"][@target="{0}"]'),
        ('pos', 'term:pos($tig) = "{0}"'),
        ('tt', 'term:type($tig) = "{0}"'),
    )

    for f in filters:
        param = _get_search_param(f[0])

        if param:
            f_str += ' and ' + f[1].format(param)

    return f_str

@search.route('/')
def results():
    page = None
    non_default = False
    q = request.args.get('q', '').strip()

    if q:
        predicate = _get_search_predicate(q)
        filter = _get_search_filters()

        field = request.args.get('field', 'term')
        non_default = filter or field != 'term'

        qs = """
        import module namespace term = "http://tzos.net/term" at "term.xqm";

        for $tig in collection($collection)//tig
        where term:is_public($tig) and {0}{1}
        return term:values($tig)
        """.format(predicate.encode('utf-8'),
                   filter.encode('utf-8'))

        pn = int(request.args.get('p', 1))
        pp = int(request.args.get('pp', 10))

        values = dbxml.get_db().raw_query(qs).as_str().all()

        items = get_terms_from_values(values)
        page = paginate(items, pn, pp)


    form = SearchForm(request.args, csrf_enabled=False)

    form.lang.choices = dropdown_list(get_dict_langs(), 'all', _('All'))
    form.concept_origin.choices = \
            dropdown_list(get_origins_dropdown(), 'all', _('All'))
    form.na_org.choices = \
            dropdown_list(get_responsible_orgs(), 'all', _('All'))
    form.subject_field.choices = \
            dropdown_list(sorted(SUBJECT_FIELDS, key=lambda x: x[1]),
                          'all', _('All'))

    ctx = {'form': form, 'q': q, 'page': page, 'non_default': non_default}
    return render_template('search/results.html', **ctx)
