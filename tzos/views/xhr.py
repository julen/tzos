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
from tzos.models import TermSource, User

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

    results = TermSource.query \
            .filter(TermSource.name.like(u'%{0}%'.format(q))).limit(5)

    result_list = []
    for source in results:
        result_list.append(source.name)

    return json.dumps(result_list)

@xhr.route('/ac/originatingPerson/')
@require_term
def originating_person(q):

    results = User.query \
            .filter(User.display_name.like(u'%{0}%'.format(q))).limit(5)

    result_list = []
    for user in results:
        result_list.append(user.display_name)

    return json.dumps(result_list)

@xhr.route('/ac/term/')
@require_term
def term(q):

    lang = request.args.get('lang', None)
    sf = request.args.get('sf', None)

    results = []

    fields = sf.split(u';')

    for field in fields:

        # FIXME: we should split subjectFields and check for each field
        qs = u'collection($collection)/martif/text/body/termEntry[descrip[@type="subjectField"]/string()="{0}"]/langSet[@xml:lang="{1}"]/tig/term[dbxml:contains(string(), "{2}")]/string()'.format(field, lang, q).encode('utf-8')

        res = dbxml.session.raw_query(qs).as_str().all()

        if res:
            results.extend(res)

    return json.dumps(sorted(results))
