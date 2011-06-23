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
from tzos.helpers import require_valid_dict
from tzos.models import Term

glossary = Module(__name__)

@glossary.route('/<string(length=2):dict>/<string(length=1):letter>/')
@require_valid_dict
def list_letter(dict, letter):

    pn = int(request.args.get('p', 1))

    qs = """
    import module namespace term = "http://tzos.net/term" at "term.xqm";

    for $tig in collection($collection)/martif/text/body/termEntry/langSet[@xml:lang="{0}"]/tig
    where $tig[starts-with(lower-case(term/string()), "{1}")] and
          (term:is_public($tig) or term:owner($tig) = "{2}")
    order by lower-case($tig/term/string()) ascending,
             $tig/term/string() descending
    return term:values($tig)
    """.format(dict.encode('utf-8'),
               letter.encode('utf-8'),
               getattr(g.user, 'username', u'').encode('utf-8'))

    page = dbxml.session.raw_query(qs). \
            as_callback(Term.parse).paginate(pn, 10)

    return render_template('glossary/list_letter.html', page=page,
                                                        letter=letter)
