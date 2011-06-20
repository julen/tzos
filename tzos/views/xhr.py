# -*- coding: utf-8 -*-
"""
    tzos.views.xhr
    ~~~~~~~~~~~~~~

    Views involving XMLHttpRequest requests.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from functools import wraps

from flask import Module, json, request

from tzos.extensions import dbxml

xhr = Module(__name__)

def require_term(f):

    @wraps(f)
    def decorator(*args, **kwargs):

        q = request.args.get('term', None)

        if not q:
            return json.dumps({})

        return f(q, *args, **kwargs)

    return decorator

@xhr.route('/ac/entrySource/')
@require_term
def entry_source(q):

    qs = u'distinct-values(collection($collection)//admin[@type="entrySource"][dbxml:contains(./string(), "{0}")]/string())'.format(q).encode('utf-8')

    results = dbxml.session.raw_query(qs).as_str().all()

    return json.dumps(results)
