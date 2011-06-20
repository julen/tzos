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

@xhr.route('/ac/entrySource/')
def entry_source():

    q = request.args.get('term', None)

    if not q:
        return json.dumps({})

    qs = u'distinct-values(collection($collection)//admin[@type="entrySource"][dbxml:contains(./string(), "{0}")]/string())'.format(q).encode('utf-8')

    results = dbxml.session.raw_query(qs).as_str().all()

    return json.dumps(results)
