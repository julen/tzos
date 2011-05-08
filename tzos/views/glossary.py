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

glossary = Module(__name__)

@glossary.route('/<string(length=2):dict>/<string(length=1):letter>/')
@require_valid_dict
def list_letter(dict, letter):

    ctx = {'lang': dict, 'letter': letter,
           'pn': int(request.args.get('p', 1)),
           'current_user': getattr(g.user, 'username', None)}
    terms = dbxml.get_db().template_query('glossary/term_detail.xq',
                                          context=ctx).as_rendered().all()

    return render_template('glossary/list_letter.html', terms=terms, letter=letter)
