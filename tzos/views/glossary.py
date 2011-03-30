# -*- coding: utf-8 -*-
"""
    tzos.views.term
    ~~~~~~~~~~~~~~~

    Term views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, abort, g, render_template, session

from flaskext.babel import gettext as _

from tzos.extensions import dbxml
from tzos.helpers import get_tzos_dicts

glossary = Module(__name__)

@glossary.route('/<string(length=2):dict>/<string(length=1):letter>/')
def list_letter(dict, letter):

    # Check if the requested dict exist, otherwise abort with 404
    available_dicts = get_tzos_dicts(only_codes=True)

    if dict not in available_dicts:
        return abort(404)

    ctx = {'lang': dict, 'letter': letter}
    terms = dbxml.get_db().template_query('glossary/xquery_term.html',
                                          context=ctx).as_rendered().all()

    return render_template('glossary/list_letter.html', terms=terms, letter=letter)
