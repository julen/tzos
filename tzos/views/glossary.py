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

    for $tig in collection($collection)//tig
    where $tig[starts-with(lower-case(term/string()), "{0}")] and
          $tig/..[@xml:lang="{1}"] and
          (term:is_public($tig) or term:owner($tig) = "{2}")
    order by $tig/term/string() ascending
    return term:values($tig)
    """.format(letter.encode('utf-8'),
               dict.encode('utf-8'),
               getattr(g.user, 'username', u'').encode('utf-8'))

    values = dbxml.get_db().raw_query(qs).as_str().all()

    items = get_terms_from_values(values)
    page = paginate(items, pn, 10)

    return render_template('glossary/list_letter.html', page=page,
                                                        letter=letter)
