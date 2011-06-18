# -*- coding: utf-8 -*-
"""
    tzos.forms.terms
    ~~~~~~~~~~~~~~~~

    Terms forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import AnyOf, BooleanField, FileField, Form, HiddenField, \
        NoneOf, Optional, SelectField, SubmitField, \
        TextAreaField, TextField, ValidationError, regexp, required

from tzos.extensions import dbxml
from tzos.forms.fields import BooleanWorkingField, OriginatingPerson, \
        SelectMultipleFieldDyn, SelectFieldPlus
from tzos.strings import *


#
# Validators
#

DISPLAY_NAME_RE = r'^[^_0-9\+]+$'
is_display_name = regexp(DISPLAY_NAME_RE,
                         message=_(u"You can only use letters."))

class NotContains(object):
    """
    Checks the incoming data doesn't contain a sequence of invalid inputs.

    :param values:
        A sequence of invalid inputs.
    :param message:
        Error message to raise in case of a validation error. `%(values)s`
        contains the value which caused the error.
    """
    def __init__(self, values, message=None):
        self.values = values
        self.message = message

    def __call__(self, form, field):
        for value in self.values:
            if value in field.data:
                if self.message is None:
                    self.message = field.gettext(u"Illegal input, can't contain ‘%(value)s’.")

                raise ValueError(self.message % {'value': value})

is_valid_input = NotContains((u'|||', u';;;'))

def check_exists(form, field):
    if field.data != u"":
        message = _(u"This term doesn't exist in the database.")

        lang = form.language.data
        term = field.data

        # FIXME: Also check in subject field?
        qs = u"//langSet[@xml:lang='{0}']/tig/term[string()='{1}']". \
                format(lang, term)
        result = dbxml.session.query(qs).as_str().first()

        if not result:
            raise ValidationError(message)

def check_required_dropdown(form, field):
    message = _(u"You must choose a valid option.")

    if not field.data or field.data in ('none',):
        raise ValidationError(message)

def check_collision(form, field):
    message = _(u"This term already exists in the database.")

    # FIXME: Also check in subject field?
    qs = u'//langSet[@xml:lang="{0}"]/tig/term[string()="{1}"]'. \
            format(form.language.data, form.term.data)
    result = dbxml.session.query(qs).as_str().first()

    if result:
        raise ValidationError(message)

def check_syntrans(form, field):
    message = _(u"You must specify a term.")

    if form.syntrans.data and field.data == "":
        raise ValidationError(message)

def check_syntrans_exists(form, field):
    if form.syntrans.data and field.data != "":
        message = _(u"This term doesn't exist in the database.")

        lang = form.syntrans_lang.data
        term = field.data

        # FIXME: Also check in subject field?
        qs = u'//langSet[@xml:lang="{0}"]/tig/term[string()="{1}"]'. \
                format(lang, term)
        result = dbxml.session.query(qs).as_str().first()

        if not result:
            raise ValidationError(message)

def check_as_is_set(form, field):
    message = _(u"Administrative status is not set.")

    if form.administrative_status.data == u'' and \
       field.data == u"consolidatedElement":
        raise ValidationError(message)

#
# Forms
#


class CoreTermForm(Form):

    def __init__(self, *args, **kwargs):
        self._do_postprocess = False

        if 'formdata' in kwargs and kwargs['formdata']:
            self._do_postprocess = True

        super(CoreTermForm, self).__init__(*args, **kwargs)

    def process(self, *args, **kwargs):
        super(CoreTermForm, self).process(*args, **kwargs)

        if self._do_postprocess:
            self.originating_person. \
                postprocess_formdata(self.originating_person.raw_data)

    def validate(self, *args):
        """Calls all field validators and if there are any errors calls
        a postrocessing function for the originating_person field.

        Returns the same boolean value as `validate` would do."""

        rv = super(CoreTermForm, self).validate(*args)

        if self.errors:
            valuelist = self.originating_person.raw_data
            self.originating_person.postprocess_formdata(valuelist)

        return rv


    concept_origin = SelectFieldPlus(_(u"Origin"),
            validators=[required(message=_(u"Origin is required."))])

    # Affects elementWorkingStatus
    working_status = BooleanWorkingField(_(u"I want this term to be public."),
            default="checked")

    subject_field = SelectMultipleFieldDyn(_(u"Subject field"),
            validators=[check_required_dropdown])

    originating_person = OriginatingPerson(_(u"Originating person"),
            description=_(u"If you leave this field blank, that means "
                          "you are the term author."),
            validators=[Optional(), is_display_name])

class BaseTermForm(CoreTermForm):

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(BaseTermForm, self).__init__(*args, **kwargs)

    #
    # Transaction-related stuff
    #
    transac_type = HiddenField(default='input',
            validators=[AnyOf('input')])

    #
    # Optional fields
    #

    ctx_desc = _(u"A text which illustrates a concept or a term by "
                 "containing the concept designation itself. "
                 "It must be authentic.")
    context = TextAreaField(_('Context'),
            description=ctx_desc,
            validators=[is_valid_input])

    xref_desc = _(u"A related term.")
    cross_reference = TextField(_(u'Cross reference'),
            description=xref_desc,
            validators=[check_exists, is_valid_input])

    def_desc = _(u"A descriptive statement which serves to differentiate "
                 "from related concepts.")
    definition = TextAreaField(_(u'Definition'),
            description=def_desc,
            validators=[is_valid_input])

    es_desc = _(u"The source of the terminological entry.")
    entry_source = TextField(_(u'Entry source'),
            description=es_desc,
            validators=[is_valid_input])

    example_desc = _(u"A text which illustrates a concept or a term. "
                     "It can be an invented sentence.")
    example = TextAreaField(_(u'Example'),
            description=example_desc,
            validators=[is_valid_input])

    explan_desc = _(u"A statement that describes and clarifies a concept "
                    "and makes it understandable, but does not necessarily "
                    "differentiate it from other concepts.")
    explanation = TextAreaField(_(u'Explanation'),
            description=explan_desc,
            validators=[is_valid_input])

    product_subset = SelectFieldPlus(_(u'Product subset'),
            choices=PRODUCT_SUBSET, placeholder='', sort=True)

    #
    # Linguistic fields
    #
    normative_authorization = SelectFieldPlus(_(u'Normative level'),
            choices=NORMATIVE_AUTHORIZATIONS, placeholder='', sort=True)
    normative_authorization_org = SelectFieldPlus(_(u'Normative organization'),
            placeholder='', sort=True)

    subordinate_concept_generic = TextField(_(u'Hyponym'),
            validators=[check_exists])
    superordinate_concept_generic = TextField(_(u'Hypernym'),
            validators=[check_exists])
    antonym_concept = TextField(_(u'Antonym'),
            validators=[check_exists])

    rltd_desc = _(u"A concept that has an associative relation to another "
                  "concept, such as teacher and school.")
    related_concept = TextField(_(u'Related concept'),
            description=rltd_desc,
            validators=[check_exists])

    part_of_speech = SelectFieldPlus(_(u'Part of Speech'),
            choices=PART_OF_SPEECH, placeholder='', sort=True,
            no_sort=('noun',))

    term_type = SelectFieldPlus(_('Term type'),
            choices=TERM_TYPES, placeholder='', sort=True)


class AddTermForm(BaseTermForm):

    term = TextField(_(u"Term"),
            validators=[required(message=_(u"Term is required.")),
                        is_valid_input,
                        check_collision])

    language = SelectFieldPlus(_(u"Language"),
            validators=[check_required_dropdown])

    syntrans = BooleanField(_(u"This term is a synonym or a "
                              "translation for another term."))

    syntrans_term = TextField(_(u"Term"),
            validators=[check_syntrans,
                        check_syntrans_exists])

    syntrans_lang = SelectFieldPlus(_(u"Language"),
            validators=[check_required_dropdown])


    submit = SubmitField(_(u"Add"))


class EditTermForm(BaseTermForm):

    language = HiddenField(_(u"Language"))

    transac_type = HiddenField(default='modification',
            validators=[AnyOf('modification')])

    submit = SubmitField(_(u"Save changes"))


class ModEditTermForm(EditTermForm):

    ws_choices = WORKING_STATUS
    ws_desc = _(u"If you consolidate this term, you must set "
                "its administrative status ('Linguistic information' tab).")
    working_status = SelectFieldPlus(_(u"Working status"),
            choices=ws_choices,
            description=ws_desc,
            validators=[check_as_is_set])

    as_desc = _(u"This field has no effect if the working status "
                "of this term is other than 'Consolidated'.")
    administrative_status = SelectFieldPlus(_(u"Administrative status "
            "within the TZOS environment"), description=as_desc,
            choices=ADMINISTRATIVE_STATUS, placeholder='', sort=True)


class UploadForm(CoreTermForm):

    file = FileField(_(u"File"))

    term_field = SelectField(_(u"Term column"))

    other_fields = SelectField()

    columns = HiddenField()

    transac_type = HiddenField(default='importation',
            validators=[AnyOf('importation')])

    submit = SubmitField(_(u"Upload"))
