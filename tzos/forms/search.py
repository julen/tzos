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

from tzos.forms.fields import DynamicSelectField

class SearchForm(Form):
    q = TextField(_('Keywords'))

    lang = DynamicSelectField(_("Language"))

    source = TextField(_('Source'))
    example = TextField(_('Examples'))
    definition = TextField(_('Definition'))
    sample = TextField(_('Sample text'))

    submit = SubmitField(_('Search'))
