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
from tzos.models import TermSource, TermSubject, User

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
    root_fields = []

    sfields = sf.split(u';')

    for code in sfields:
        root_codes = TermSubject.root_codes(code)

        if root_codes:
            root_fields.extend(root_codes)

    root_fields = set(root_fields)

    # FIXME: we should look on parent subject fields too
    qs = u'''
    import module namespace term = "http://tzos.net/term" at "term.xqm";

    for $tig in collection($collection)/martif/text/body/termEntry/langSet[@xml:lang="{0}"]/tig[term[dbxml:contains(string(), "{1}")]]
    where (let $fields := tokenize(term:subject_field($tig), ";") return some $f in $fields satisfies $f = tokenize("{2}", ";"))
    return term:term($tig)
    '''.format(lang, q, u";".join(root_fields)).encode('utf-8')

    results = dbxml.session.raw_query(qs).as_str().all()

    return json.dumps(sorted(results))
