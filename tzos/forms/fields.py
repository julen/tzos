# -*- coding: utf-8 -*-
"""
    tzos.forms.fields
    ~~~~~~~~~~~~~~~~~

    Custom form fields.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from operator import itemgetter

from flask import g

from flaskext.babel import lazy_gettext as _
from flaskext.wtf import BooleanField, SelectField, \
        SelectMultipleField, TextField

from tzos.models import TermSubject


class SelectFieldPlus(SelectField):
    """A SelectField which can be sorted and set default placeholder values.

    This also allows disabling pre validation, which complicates
    stuff when using validators in dynamic select fields."""

    PLACEHOLDERS = {
        -1: _(u'Top-level element'),
        '': u'----',
        'all': _(u'All'),
    }

    def __init__(self, label=None, validators=None, coerce=unicode, \
            choices=None, placeholder=None, sort=False, \
            no_sort=(), pre_validation=False, **kwargs):

        self.pre_validation = pre_validation

        self.placeholder = placeholder
        self.sort = sort
        self.sort_exceptions = no_sort

        super(SelectFieldPlus, self).__init__(label, validators, \
                coerce, choices, **kwargs)

    def iter_choices(self):
        """Do some black magic before yelding values."""

        no_sort = []
        choices = self.choices[:]

        if self.sort_exceptions and self.sort:

            for ex in self.sort_exceptions:
                try:
                    i = map(itemgetter(0), choices).index(ex)
                    no_sort.insert(0, choices.pop(i))
                except ValueError:
                    pass

        if self.sort:
            self.choices = sorted(choices, key=lambda x: x[1])

        # If there are exceptions we don't want to sort, insert them
        # at the beginning of the choices list
        map(lambda x: self.choices.insert(0, x), no_sort)

        try:
            value = self.PLACEHOLDERS[self.placeholder]
        except KeyError:
            value = None

        if value:
            self.choices.insert(0, (self.placeholder, value))

        return super(SelectFieldPlus, self).iter_choices()

    def pre_validate(self, form):
        if self.pre_validation:
            for v, _ in self.choices:
                if self.data == v:
                    break
            else:
                raise ValueError(_(u'Not a valid choice'))


class SelectMultipleFieldDyn(SelectMultipleField):

    def __init__(self, label=None, validators=None, coerce=unicode, \
            choices=None, pre_validation=False, **kwargs):

        self.pre_validation = pre_validation

        super(SelectMultipleFieldDyn, self).__init__(label, validators, \
                coerce, choices, **kwargs)

    def pre_validate(self, form):
        if self.pre_validation:
            if self.data:
                values = list(c[0] for c in self.choices)
                for d in self.data:
                    if d not in values:
                        raise ValueError(self.gettext(u"'%(value)s' is not a valid choice for this field") % dict(value=d))


class SubjectField(SelectMultipleFieldDyn):
    """A SelectMultipleField that sets root subject fields even if the
    user hasn't set any."""

    def process_formdata(self, valuelist):

        try:
            if isinstance(valuelist[0], list):
                valuelist = valuelist[0]
        except IndexError:
            pass

        root_codes = list(set([unicode(TermSubject.root_code(c)) \
                for c in valuelist]))
        root_codes.extend(valuelist)

        self.data = list(set(root_codes))


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


class MultipleTextField(TextField):
    """A TextField which will allow multiple `items` in the UI."""

    def process_data(self, value):
        if value:
            self.data = u";;;".join(value)
        else:
            self.data = u""


class OriginatingPerson(MultipleTextField):
    """A TextField for defining originatingPerson fields."""

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0] == u"":
            self.data = g.user.display_name or g.user.username
        else:
            try:
                self.data = valuelist[0]
            except IndexError:
                self.data = u""
