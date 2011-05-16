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
from tzos.helpers import dropdown_list
from tzos.strings import *

class SearchForm(Form):
    q = TextField(_('Keywords'))

    lang = DynamicSelectField(_("Language"))

    sf_choices = dropdown_list(SUBJECT_FIELDS, 'all', _('All'))
    subject_field = DynamicSelectField(_('Subject field'), choices=sf_choices)

    source = TextField(_('Source'))
    example = TextField(_('Examples'))
    definition = TextField(_('Definition'))
    sample = TextField(_('Sample text'))

    submit = SubmitField(_('Search'))
