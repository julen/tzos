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

from tzos.forms.fields import SelectFieldPlus
from tzos.strings import *

class SearchForm(Form):

    q = TextField(_('Keywords'))

    lang = SelectFieldPlus(_("Language"), placeholder='all', sort=True)

    #
    # Filtering mode
    #
    mode_choices = (
        ('and', _(u"All conditions must be met (AND style search).")),
        ('or', _(u"Any of the conditions must be met (OR style search)."))
    )
    mode = RadioField(_(u"Search mode"), default=u"and", choices=mode_choices)

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
    field = SelectFieldPlus(_('Search field'), default='term',
            choices=field_choices, sort=True)

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
    subject_field = SelectFieldPlus(_('Subject field'),
            placeholder='all')

    product_subset = SelectFieldPlus(_('Appears in'),
            choices=PRODUCT_SUBSET, placeholder='all', sort=True)

    concept_origin = SelectFieldPlus(_("Origin"),
            placeholder='all')

    #
    # Linguistic information
    #
    na = SelectFieldPlus(_('Normative level'),
            choices=NORMATIVE_AUTHORIZATIONS, placeholder='all', sort=True)

    na_org = SelectFieldPlus(_('Normative organization'),
            placeholder='all', sort=True)

    pos = SelectFieldPlus(_('Part of Speech'), choices=PART_OF_SPEECH,
            placeholder='all', sort=True, no_sort=('noun',))

    tt = SelectFieldPlus(_('Term type'), choices=TERM_TYPES,
            placeholder='all', sort=True)

    submit = SubmitField(_('Search'))
