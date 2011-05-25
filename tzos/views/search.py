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
        get_origins_dropdown, get_responsible_orgs
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
        'term': '$term/string()',
        'definition': '$term/../../descrip[@type="definition"]/string()',
        'context': '$term/../descrip[@type="context"]/string()',
        'example': '$term/../descrip[@type="example"]/string()',
        'explanation': '$term/../descrip[@type="explanation"]/string()',
        'hyponym': '$term/../../../descrip[@type="subordinateConceptGeneric"]/string()',
        'hypernym': '$term/../../../descrip[@type="superordinateConceptGeneric"]/string()',
        'antonym': '$term/../../../descrip[@type="antonymConcept"]/string()',
        'related': '$term/../../../descrip[@type="relatedConcept"]/string()',
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
        ('lang', '$term/../..[@xml:lang="{0}"]'),
        ('subject_field', '(let $fields := tokenize(term:subject_field($term), ";") return some $f in $fields satisfies $f = "{0}")'),
        ('product_subset', '$term/../admin[@type="productSubset"]/string() = "{0}"'),
        ('concept_origin', '$term/../admin[@type="conceptOrigin"]/string() = "{0}"'),
        ('na', '$term/../termNote[@type="normativeAuthorization"]/string() = "{0}"'),
        ('na_org', '$term/../termNote[@type="normativeAuthorization"][@target="{0}"]'),
        ('pos', '$term/../termNote[@type="partOfSpeech"]/string() = "{0}"'),
        ('tt', '$term/../termNote[@type="termType"]/string() = "{0}"'),
    )

    for f in filters:
        param = _get_search_param(f[0])

        if param:
            f_str += ' and ' + f[1].format(param)

    return f_str

@search.route('/')
def quick():
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

        for $term in collection($collection)//term
        where term:is_public($term) and {0}{1}
        return term:asLink($term)
        """.format(predicate.encode('utf-8'),
                   filter.encode('utf-8'))

        pn = int(request.args.get('p', 1))
        pp = int(request.args.get('pp', 10))

        page = dbxml.get_db().raw_query(qs).as_rendered(). \
                                            paginate(pn, pp, error_out=False)

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
