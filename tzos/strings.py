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

TERM_TYPES = [
    ('abbreviation', _('Abbreviation')),
    ('acronym', _('Acronym')),
    ('clippedTerm', _('Clipped term')),
    ('commonName', _('Common name')),
    ('entryTerm', _('Entry term')),
    ('equation', _('Equation')),
    ('formula', _('Formula')),
    ('fullForm', _('Full form')),
    ('initialism', _('Initialism')),
    ('internationalism', _('Internationalism')),
    ('internationalScientificTerm', _('International scientific term')),
    ('logicalExpression', _('Logical expression')),
    ('partNumber', _('Part number')),
    ('phraseologicalUnit', _('Phraseological unit')),
    ('transcribedForm', _('Transcribed form')),
    ('transliteratedForm', _('Transliterated form')),
    ('shortForm', _('Short form')),
    ('shortcut', _('Shortcut')),
    ('sku', _('SKU (Stock Keeping Unit)')),
    ('standardText', _('Standard text')),
    ('string', _('String')),
    ('symbol', _('Symbol')),
    ('synonym', _('Synonym')),
    ('synonymousPhrase', _('Synonymous phrase')),
    ('variant', _('Variant')),
    ('other', _('Other')),
]
