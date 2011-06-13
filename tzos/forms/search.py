# -*- coding: utf-8 -*-
"""
    tzos.forms.search
    ~~~~~~~~~~~~~~~~~

    Search forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import Form, RadioField, SelectField, SubmitField, TextField

from tzos.forms.fields import DynamicSelectField
from tzos.helpers import dropdown_list
from tzos.strings import *

class SearchForm(Form):
    q = TextField(_('Keywords'))

    lang = DynamicSelectField(_("Language"))

    #
    # Filtering mode
    #
    mode_choices = (
        ('and', _(u"All conditions must be met (AND style search).")),
        ('or', _(u"Any of the conditions must be met (OR style search)."))
    )
    mode = RadioField(_(u"Search mode"), choices=mode_choices)

    #
    # General
    #
    field_choices = (
        ('term', _('Term')),
        ('definition', _('Definition')),
        ('context', _('Context')),
        ('example', _('Example')),
        ('explanation', _('Explanation')),
        ('hyponym', _('Hyponym')),
        ('hypernym', _('Hypernym')),
        ('antonym', _('Antonym')),
        ('related', _('Related concept')),
    )
    field = SelectField(_('Search field'), choices=field_choices)

    pp_choices = (
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
    )
    pp = SelectField(_('Terms per page'), choices=pp_choices)

    #
    # Classification
    #
    sf_choices = dropdown_list(SUBJECT_FIELDS, 'all', _('All'))
    subject_field = DynamicSelectField(_('Subject field'), choices=sf_choices)

    ps_choices = dropdown_list(PRODUCT_SUBSET, 'all', _('All'))
    product_subset = SelectField(_('Appears in'), choices=ps_choices)

    concept_origin = SelectField(_("Origin"))

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
