# -*- coding: utf-8 -*-
"""
    tzos.forms.search
    ~~~~~~~~~~~~~~~~~

    Search forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import Form, SubmitField, TextField

class SearchForm(Form):
    term = TextField(_('Search terms'))
    source = TextField(_('Source'))
    example = TextField(_('Examples'))
    definition = TextField(_('Definition'))
    sample = TextField(_('Sample text'))

    submit = SubmitField(_('Search'))
