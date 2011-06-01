# -*- coding: utf-8 -*-
"""
    tzos.views.glossary
    ~~~~~~~~~~~~~~~~~~~

    Glossary views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, g, render_template, request

from flaskext.babel import gettext as _

from tzos.extensions import dbxml
from tzos.helpers import get_terms_from_values, require_valid_dict
from tzos.pagination import paginate

glossary = Module(__name__)

@glossary.route('/<string(length=2):dict>/<string(length=1):letter>/')
@require_valid_dict
def list_letter(dict, letter):

    pn = int(request.args.get('p', 1))

    qs = """
    import module namespace term = "http://tzos.net/term" at "term.xqm";

    for $term in collection($collection)//term
    let $workingStatus := $term/../admin[@type="elementWorkingStatus"]/string()
    where $term[starts-with(lower-case(string()), "{0}")] and $term/../..[@xml:lang="{1}"] and (term:is_public($term) or term:owner($term) = "{2}")
    order by $term/string() ascending
    return term:values($term)
    """.format(letter.encode('utf-8'),
               dict.encode('utf-8'),
               getattr(g.user, 'username', u'').encode('utf-8'))

    values = dbxml.get_db().raw_query(qs).as_str().all()

    items = get_terms_from_values(values)
    page = paginate(items, pn, 10)

    return render_template('glossary/list_letter.html', page=page, letter=letter)
