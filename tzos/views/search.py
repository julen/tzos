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
from tzos.helpers import get_dict_langs, get_origins_dropdown, \
        get_responsible_orgs, get_sfields_dropdown
from tzos.models import Term
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

def _get_search_filters(or_search=False):

    operator = u" or " if or_search else u" and "

    filters = (
        ('lang', u'$tig/..[@xml:lang="{0}"]'),
        ('subject_field', u'(let $fields := tokenize(term:subject_field($tig), ";") return some $f in $fields satisfies $f = "{0}")'),
        ('product_subset', u'term:product_subset($tig) = "{0}"'),
        ('concept_origin', u'term:concept_origin($tig) = "{0}"'),
        ('na', u'term:norm_auth($tig) = "{0}"'),
        ('na_org', u'$tig/termNote[@type="normativeAuthorization"][@target="{0}"]'),
        ('pos', u'term:pos($tig) = "{0}"'),
        ('tt', u'term:type($tig) = "{0}"'),
    )

    result = []
    for f in filters:
        param = _get_search_param(f[0])

        if param:
            result.append(f[1].format(param))

    rv = operator.join(result)
    if rv:
        rv = u" and {0}".format(rv)

    return rv

@search.route('/')
def results():

    page = None
    q = request.args.get('q', '').strip()

    if q:
        predicate = _get_search_predicate(q)

        mode = request.args.get('mode', False)
        or_search = True if mode == u'or' else False
        filter = _get_search_filters(or_search=or_search)

        field = request.args.get('field', 'term')

        qs = """
        import module namespace term = "http://tzos.net/term" at "term.xqm";

        for $tig in collection($collection)/martif/text/body/termEntry/langSet/tig
        where term:is_public($tig) and {0}{1}
        order by term:sortkey($tig) ascending, term:term($tig) ascending
        return term:values($tig, false())
        """.format(predicate.encode('utf-8'),
                   filter.encode('utf-8'))

        pn = int(request.args.get('p', 1))
        pp = int(request.args.get('pp', 10))

        page = dbxml.session.raw_query(qs). \
                as_callback(Term.parse).paginate(pn, pp)

    form = SearchForm(request.args, csrf_enabled=False)

    form.lang.choices = get_dict_langs()
    form.concept_origin.choices = get_origins_dropdown()
    form.subject_field.choices = get_sfields_dropdown(g.ui_lang)
    form.na_org.choices = get_responsible_orgs()

    ctx = {'form': form, 'q': q, 'page': page, 'show_options': not q}
    return render_template('search/results.html', **ctx)
