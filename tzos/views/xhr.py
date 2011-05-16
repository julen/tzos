# -*- coding: utf-8 -*-
"""
    tzos.views.xhr
    ~~~~~~~~~~~~~~

    Views involving XMLHttpRequest requests.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, json, request

from tzos.extensions import dbxml

xhr = Module(__name__)

@xhr.route('/autocomplete/')
def autocomplete():

    t = request.args.get('type', None)
    q = request.args.get('term', None)

    if not t or not q:
        return json.dumps({})

    type_map = {
        'entrySource': 'distinct-values(collection($collection)//admin[@type="entrySource"][dbxml:contains(./string(), "{0}")]/string())',
    }

    try:
        qs = type_map[t].format(q)
    except KeyError:
        qs = None

    results = []

    if qs:
        results = dbxml.get_db().raw_query(qs).as_str().all()

    print qs
    print results

    return json.dumps(results)