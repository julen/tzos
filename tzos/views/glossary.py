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

    ctx = {'lang': dict, 'letter': letter,
           'current_user': getattr(g.user, 'username', '')}

    pn = int(request.args.get('p', 1))

    values = dbxml.get_db().template_query('glossary/term_detail.xq',
                                           context=ctx).as_str().all()

    items = get_terms_from_values(values)
    page = paginate(items, pn, 10)

    return render_template('glossary/list_letter.html', page=page, letter=letter)
