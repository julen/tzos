# -*- coding: utf-8 -*-
"""
    tzos.forms.terms
    ~~~~~~~~~~~~~~~~

    Terms forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import AnyOf, BooleanField, FieldList, FileField, Form, \
        HiddenField, Optional, SelectField, SubmitField, TextAreaField, \
        TextField, ValidationError, regexp, required

from tzos.extensions import dbxml
from tzos.forms.fields import BooleanWorkingField, MultipleTextField, \
        OriginatingPerson, SelectMultipleFieldDyn, SelectFieldPlus, SubjectField
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

def check_required_dropdown(form, field):
    message = _(u"You must choose a valid option.")

    if not field.data or field.data in ('none',):
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
        sfields = form.subject_field.data

        qs = '''
        import module namespace term = "http://tzos.net/term" at "term.xqm";

        for $tig in collection($collection)/martif/text/body/termEntry/langSet[@xml:lang="{0}"]/tig
        where term:is_public($tig) and
              term:term($tig) = "{1}" and
              (let $fields := tokenize(term:subject_field($tig), ";;;")
              return some $f in $fields satisfies $f = $sfields)
        return term:term($tig)
        '''.format(lang, term.encode('utf-8'))

        ctx = {'sfields': sfields}

        result = dbxml.session.raw_query(qs, ctx).as_str().first()

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

    concept_origin = SelectMultipleFieldDyn(_(u"Origin"),
            validators=[required(message=_(u"Origin is required."))])

    subject_field = SubjectField(_(u"Subject field"),
            validators=[check_required_dropdown])

    originating_person = OriginatingPerson(_(u"Originating person"),
            description=_(u"If you leave this field blank, that means "
                          "you are the term author."),
            validators=[Optional(), is_display_name])

class BaseTermForm(CoreTermForm):

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(BaseTermForm, self).__init__(*args, **kwargs)

    term = TextField(_(u"Term"),
            validators=[required(message=_(u"Term is required.")),
                        is_valid_input])

    #
    # Transaction-related stuff
    #
    transac_type = HiddenField(default='input',
            validators=[AnyOf('input')])

    #
    # Optional fields
    #

    xref_desc = _(u"A related term.")
    cross_reference = MultipleTextField(_(u'Cross reference'),
            description=xref_desc)

    es_desc = _(u"The source of the terminological entry.")
    entry_source = MultipleTextField(_(u'Entry source'),
            description=es_desc)

    def_desc = _(u"A descriptive statement which serves to differentiate "
                 "from related concepts.")
    definition = FieldList(TextAreaField(_(u'Definition'),
            description=def_desc), min_entries=1)

    ctx_desc = _(u"A text which illustrates a concept or a term by "
                 "containing the concept designation itself. "
                 "It must be authentic.")
    context = FieldList(TextAreaField(_('Context'),
            description=ctx_desc), min_entries=1)

    example_desc = _(u"A text which illustrates a concept or a term. "
                     "It can be an invented sentence.")
    example = FieldList(TextAreaField(_(u'Example'),
            description=example_desc), min_entries=1)

    explan_desc = _(u"A statement that describes and clarifies a concept "
                    "and makes it understandable, but does not necessarily "
                    "differentiate it from other concepts.")
    explanation = FieldList(TextAreaField(_(u'Explanation'),
            description=explan_desc), min_entries=1)

    product_subset = SelectMultipleFieldDyn(_(u'Product subset'),
            choices=PRODUCT_SUBSET)

    #
    # Linguistic fields
    #
    normative_authorization = SelectFieldPlus(_(u'Normative level'),
            choices=NORMATIVE_AUTHORIZATIONS, placeholder='', sort=True)
    normative_authorization_org = SelectFieldPlus(_(u'Normative organization'),
            placeholder='', sort=True)

    subordinate_concept_generic = MultipleTextField(_(u'Hyponym'))
    superordinate_concept_generic = MultipleTextField(_(u'Hypernym'))
    antonym_concept = MultipleTextField(_(u'Antonym'))

    rltd_desc = _(u"A concept that has an associative relation to another "
                  "concept, such as teacher and school.")
    related_concept = MultipleTextField(_(u'Related concept'),
            description=rltd_desc)

    part_of_speech = SelectFieldPlus(_(u'Part of Speech'),
            choices=PART_OF_SPEECH, placeholder='', sort=True,
            no_sort=('noun',))

    term_type = SelectFieldPlus(_('Term type'),
            choices=TERM_TYPES, placeholder='', sort=True)


class AddTermForm(BaseTermForm):

    language = SelectFieldPlus(_(u"Language"),
            validators=[check_required_dropdown])

    working_status = HiddenField(default=u"starterElement",
            validators=[AnyOf((u"starterElement",))])

    # l10n: Follows a dropdown box with language names
    eqlang = SelectFieldPlus(_(u"Add equivalent in"), placeholder='')

    syntrans = BooleanField(_(u"This term is a synonym or a "
                              "translation for another term."))

    syntrans_term = TextField(_(u"Term"),
            validators=[check_syntrans,
                        check_syntrans_exists])

    syntrans_lang = SelectFieldPlus(_(u"Language"),
            validators=[Optional(), check_required_dropdown])

    submit = SubmitField(_(u"Add"))


    @property
    def eqterm_fields(self):
        fields = [getattr(self, f) for f in self._fields \
                if f.startswith('eqterm-')]
        return sorted(fields)


class AddTermFormCor(AddTermForm):
    """AddTermForm for users with `is_corrector` privileges."""

    working_status = BooleanWorkingField(_(u"I want this term to be public."),
            default="checked")


class CollisionForm(AddTermForm):

    discard = SubmitField(_(u"No, discard my term"))
    force = SubmitField(_(u"Yes, insert my term"))

class CollisionFormCor(CollisionForm, AddTermFormCor):

    pass

class EditTermForm(BaseTermForm):

    language = HiddenField(_(u"Language"))

    transac_type = HiddenField(default='modification',
            validators=[AnyOf('modification')])

    submit = SubmitField(_(u"Save changes"))


class EditTermFormCor(EditTermForm):
    """EditTermForm for users with `is_corrector` privileges."""

    working_status = BooleanWorkingField(_(u"I want this term to be public."))


class EditTermFormMod(EditTermForm):
    """EditTermForm for users with `is_moderator` privileges."""

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

    working_status = HiddenField(default=u"starterElement",
            validators=[AnyOf((u"starterElement",))])

    fpath = HiddenField()

    file = FileField(_(u"File"))

    term_field = SelectField(_(u"Term column"))

    other_fields = SelectField()

    columns = HiddenField()

    transac_type = HiddenField(default='importation',
            validators=[AnyOf('importation')])

    submit = SubmitField(_(u"Upload"))

    confirm = SubmitField(_(u"Confirm"))
    cancel = SubmitField(_(u"Cancel"))

class UploadFormCor(UploadForm):
    """UploadForm for users with `is_corrector` privileges."""

    working_status = BooleanWorkingField(_(u"I want these terms to be public."),
            default="checked")
