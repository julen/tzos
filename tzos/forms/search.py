# -*- coding: utf-8 -*-
"""
    tzos.forms.search
    ~~~~~~~~~~~~~~~~~

    Search forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import Form, SelectField, SubmitField, TextField

from tzos.forms.fields import DynamicSelectField
from tzos.helpers import dropdown_list
from tzos.strings import *

class SearchForm(Form):
    q = TextField(_('Keywords'))

    lang = DynamicSelectField(_("Language"))

    #
    # Search fields
    #
    field_choices = (
        ('term', _('Term')),
        ('definition', _('Definition')),
        ('context', _('Context')),
        ('example', _('Example')),
        ('description', _('Description')),
        ('hyponym', _('Hyponym')),
        ('hyperonym', _('Hyperonym')),
        ('antonym', _('Antonym')),
        ('related', _('Related concept')),
    )
    field = SelectField(_('Search field'), choices=field_choices)

    #
    # Classification
    #
    sf_choices = dropdown_list(SUBJECT_FIELDS, 'all', _('All'))
    subject_field = DynamicSelectField(_('Subject field'), choices=sf_choices)

    concept_origin = TextField(_('Origin'))

    #
    # Linguistic information
    #
    na_choices = dropdown_list(NORMATIVE_AUTHORIZATIONS, 'all', _('All'))
    na = SelectField(_('Normative level'),
                                          choices=na_choices)

    na_org = SelectField(_('Normative organization'))

    pos_choices = dropdown_list(PART_OF_SPEECH, 'all', _('All'))
    pos = SelectField(_('Part of Speech'), choices=pos_choices)

    tt_choices = dropdown_list(TERM_TYPES, 'all', _('All'))
    tt = SelectField(_('Term type'), choices=tt_choices)

    submit = SubmitField(_('Search'))
