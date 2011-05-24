# -*- coding: utf-8 -*-
"""
    tzos.forms.fields
    ~~~~~~~~~~~~~~~~~

    Custom form fields.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import BooleanField, SelectField

class DynamicSelectField(SelectField):
    """A SelectField that allows disabling pre validation, which complicates
    stuff when using validators in dynamic select fields."""

    def __init__(self, label=None, validators=None, coerce=unicode, \
                 choices=None, pre_validation=False, **kwargs):
        super(DynamicSelectField, self).__init__(label, validators, coerce, \
                                           choices, **kwargs)

        self.pre_validation = pre_validation

    def pre_validate(self, form):
        if self.pre_validation:
            for v, _ in self.choices:
                if self.data == v:
                    break
            else:
                raise ValueError(_(u'Not a valid choice'))


class BooleanWorkingField(BooleanField):
    """A BooleanField that sets specific data according to the choice made."""

    def process_formdata(self, valuelist):
        try:
            if valuelist[0] == u'y':
                self.data = 'workingElement'
            else:
                self.data = 'starterElement'
        except IndexError:
            self.data = 'starterElement'
