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
        NoneOf, SelectField, SelectMultipleField, SubmitField, TextAreaField, \
        TextField, ValidationError, required

from tzos.extensions import dbxml
from tzos.forms.fields import BooleanWorkingField, DynamicSelectField
from tzos.helpers import dropdown_list
from tzos.strings import *


#
# Validators
#

def check_exists(form, field):
    if field.data != "":
        message = _("This term doesn't exist in the database.")

        lang = form.language.data
        term = field.data

        # FIXME: Also check in subject field?
        qs = u"//langSet[@xml:lang='{0}']/tig/term[string()='{1}']". \
                format(lang, term)
        result = dbxml.get_db().query(qs).as_str().first()

        if not result:
            raise ValidationError(message)

def check_required_dropdown(form, field):
    message = _("You must choose a valid option.")

    if not field.data or field.data in ('none',):
        raise ValidationError(message)

def check_collision(form, field):
    message = _("This term already exists in the database.")

    # FIXME: Also check in subject field?
    qs = u'//langSet[@xml:lang="{0}"]/tig/term[string()="{1}"]'. \
            format(form.language.data, form.term.data)
    result = dbxml.get_db().query(qs).as_str().first()

    if result:
        raise ValidationError(message)

def check_syntrans(form, field):
    message = _("You must specify a term.")

    if form.syntrans.data and field.data == "":
        raise ValidationError(message)

def check_syntrans_exists(form, field):
    if form.syntrans.data and field.data != "":
        message = _("This term doesn't exist in the database.")

        lang = form.syntrans_lang.data
        term = field.data

        # FIXME: Also check in subject field?
        qs = u'//langSet[@xml:lang="{0}"]/tig/term[string()="{1}"]'. \
                format(lang, term)
        result = dbxml.get_db().query(qs).as_str().first()

        if not result:
            raise ValidationError(message)

def check_not_mine(form, field):
    message = _("You must specify the author's name.")

    if form.not_mine.data and field.data == "":
        raise ValidationError(message)

def check_as_is_set(form, field):
    message = _("Administrative status is not set.")

    if form.administrative_status.data == 'none' and \
       field.data == "consolidatedElement":
        raise ValidationError(message)

#
# Forms
#


class BaseTermOriginForm(Form):

    name = TextField(validators=[
                     required(message=_("Name is required."))])

    parent_id = DynamicSelectField(_("Parent"), coerce=int)

class AddTermOriginForm(BaseTermOriginForm):

    submit = SubmitField(_("Create"))

class EditTermOriginForm(BaseTermOriginForm):

    submit = SubmitField(_("Edit"))


class CoreTermForm(Form):

    concept_origin = DynamicSelectField(_("Origin"), validators=[
        required(message=_("Origin is required."))])

    # Affects elementWorkingStatus
    working_status = BooleanWorkingField(_("I want this term to be public."))

    subject_field = SelectMultipleField(_("Subject field"), validators=[
        check_required_dropdown])

    originating_person = TextField(_("Author"),
        description=_("If you leave this field blank, that means "
                      "you are the term author."))

class BaseTermForm(CoreTermForm):

    #
    # Transaction-related stuff
    #
    transac_type = HiddenField(default='input', validators=[AnyOf('input')])

    #
    # Optional fields
    #

    ctx_desc = _("A text which illustrates a concept or a term by "
                 "containing the concept designation itself. "
                 "It must be authentic.")
    context = TextAreaField(_('Context'), description=ctx_desc)

    xref_desc = _("A related term.")
    cross_reference = TextField(_('Cross reference'), description=xref_desc,
                                validators=[check_exists])

    def_desc = _("A descriptive statement which serves to differentiate "
                 "from related concepts.")
    definition = TextAreaField(_('Definition'), description=def_desc)

    es_desc = _("The source of the terminological entry.")
    entry_source = TextField(_('Entry source'), description=es_desc)

    example_desc = _("A text which illustrates a concept or a term. "
                     "It can be an invented sentence.")
    example = TextAreaField(_('Example'), description=example_desc)

    explan_desc = _("A statement that describes and clarifies a concept "
                    "and makes it understandable, but does not necessarily "
                    "differentiate it from other concepts.")
    explanation = TextAreaField(_('Explanation'), description=explan_desc)

    ps_choices = dropdown_list(PRODUCT_SUBSET)
    product_subset = SelectField(_('Appears in'), choices=ps_choices)

    #
    # Linguistic fields
    #
    na_choices = dropdown_list(NORMATIVE_AUTHORIZATIONS)
    normative_authorization = SelectField(_('Normative authorization'),
                                          choices=na_choices)
    normative_authorization_org = SelectField(_('Organization'))

    subordinate_concept_generic = TextField(_('Hyponym'), validators=[
        check_exists])
    superordinate_concept_generic = TextField(_('Hypernym'), validators=[
        check_exists])
    antonym_concept = TextField(_('Antonym'), validators=[
        check_exists])

    rltd_desc = _("A concept that has an associative relation to another "
                  "concept, such as teacher and school.")
    related_concept = TextField(_('Related concept'), description=rltd_desc,
                                validators=[check_exists])

    pos_choices = dropdown_list(PART_OF_SPEECH)
    part_of_speech = SelectField(_('Part of Speech'), choices=pos_choices)

    tt_choices = dropdown_list(TERM_TYPES)
    term_type = SelectField(_('Term type'), choices=tt_choices)


class AddTermForm(BaseTermForm):

    term = TextField(_("Term"), validators=[
        required(message=_("Term is required.")),
        check_collision])

    language = DynamicSelectField(_("Language"), validators=[
        check_required_dropdown])

    syntrans = BooleanField(_("This term is a synonym or a "
                              "translation for another term."))

    syntrans_term = TextField(_("Term"), validators=[
        check_syntrans,
        check_syntrans_exists])

    syntrans_lang = DynamicSelectField(_("Language"), validators=[
        check_required_dropdown])

    not_mine = BooleanField(_("The author of this term is another person."))
    originating_person = TextField(_("Author"), validators=[
        check_not_mine])


    submit = SubmitField(_("Add"))


class EditTermForm(BaseTermForm):

    language = HiddenField(_("Language"))

    submit = SubmitField(_("Save changes"))


class ModEditTermForm(EditTermForm):

    ws_choices = WORKING_STATUS
    ws_desc = _("If you consolidate this term, you must set "
                "its administrative status ('Linguistic information' tab).")
    working_status = DynamicSelectField(_("Working status"),
            choices=ws_choices, description=ws_desc,
            validators=[check_as_is_set])

    as_choices = dropdown_list(ADMINISTRATIVE_STATUS)
    as_desc = _("This field has no effect if the working status "
                "of this term is other than 'Consolidated'.")
    administrative_status = DynamicSelectField(_("Administrative status "
        "within the TZOS environment"),
        choices=as_choices)


class UploadForm(CoreTermForm):

    file_desc = _("Allowed file extensions: .csv and .txt")
    file = FileField(_("File"), description=file_desc)

    submit = SubmitField(_("Upload"))
