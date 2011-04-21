# -*- coding: utf-8 -*-
"""
    strings.py
    ~~~~~~~~~~

    Special variables that need i18n love and can't be stored elsewhere.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _

NORMATIVE_AUTHORIZATIONS = [
    ('none', _('Undefined')),
    ('standardizedTerm', _('Standard')),
    ('preferredTerm', _('Preferred')),
    ('admittedTerm', _('Admitted')),
    ('deprecatedTerm', _('Deprecated')),
    ('supersededTerm', _('Superseded')),
    ('legalTerm', _('Legal')),
    ('regulatedTerm', _('Regulated')),
    ('encodedTerm', _('Encoded')),
    ('usedTerm', _('Used'))
]
