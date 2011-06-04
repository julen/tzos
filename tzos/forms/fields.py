# -*- coding: utf-8 -*-
"""
    tzos.forms.fields
    ~~~~~~~~~~~~~~~~~

    Custom form fields.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import g

from flaskext.babel import lazy_gettext as _
from flaskext.wtf import BooleanField, SelectField, TextField

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

class OriginatingPerson(TextField):
    """A TextField for defining originatingPerson fields."""

    def process_data(self, value):
        if value and value.startswith(u"_"):
            self.data = u''
        else:
            self.data = value

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0] != u'':
            self.data = valuelist[0]
        else:
            # As underscores are forbidden for usernames, we use this
            # character to differentiate from non-system names.
            self.data = u"_" + g.user.username

    def postprocess_formdata(self, valuelist):
        """This is called if validation fails and there are errors so
        formdata can be postprocessed."""

        # No username given so let's overwrite what `process_formdata`
        # could have processed.
        if valuelist and valuelist[0] == u'':
            self.data = valuelist[0]
