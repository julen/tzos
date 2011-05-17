# -*- coding: utf-8 -*-
"""
    tzos.forms.terms
    ~~~~~~~~~~~~~~~~

    Terms forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import AnyOf, BooleanField, Form, HiddenField, NoneOf, \
    SelectField, SubmitField, TextAreaField, TextField, ValidationError, required

from tzos.extensions import dbxml
from tzos.forms.fields import DynamicSelectField
from tzos.helpers import dropdown_list
from tzos.strings import *

class BaseTermForm(Form):

    def check_collision(form, field):
        message = _("This term already exists in the database.")

        # FIXME: Also check in subject field?
        qs = "//langSet[@xml:lang='{0}']/tig/term[string()='{1}']". \
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
            qs = u"//langSet[@xml:lang='{0}']/tig/term[string()='{1}']". \
                    format(lang, term)
            result = dbxml.get_db().query(qs).as_str().first()

            if not result:
                raise ValidationError(message)

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

    def check_not_mine(form, field):
        message = _("You must specify the author's name.")

        if form.not_mine.data and field.data == "":
            raise ValidationError(message)

    def check_required_dropdown(form, field):
        message = _("You must choose a valid option.")

        if not field.data or field.data in ('none',):
            raise ValidationError(message)


    #
    # Core fields
    #

    term = TextField(_("Term"), validators=[
        required(message=_("Term is required.")),
        check_collision])

    language = DynamicSelectField(_("Language"), validators=[
        check_required_dropdown])


    concept_origin = TextField(_("Origin"), validators=[
        required(message=_("Origin is required."))])

    # Affects elementWorkingStatus
    make_public = BooleanField(_("I want this term to be public immediately."))

    sf_choices = dropdown_list(SUBJECT_FIELDS)
    subject_field = DynamicSelectField(_("Subject field"), validators=[
        check_required_dropdown],
        choices=sf_choices)


    syntrans = BooleanField(_("This term is a synonym or a translation for another term."))

    syntrans_term = TextField(_("Term"), validators=[
        check_syntrans,
        check_syntrans_exists])

    syntrans_lang = DynamicSelectField(_("Language"), validators=[
        check_required_dropdown])


    not_mine = BooleanField(_("The author of this term is another person."))
    originating_person = TextField(_("Author"), validators=[
        check_not_mine])

    #
    # Transaction-related stuff
    #
    transac_type = HiddenField(default='input', validators=[AnyOf('input')])

    #
    # Optional fields
    #
    context = TextAreaField(_('Context'))
    cross_reference = TextField(_('Cross reference'), validators=[
        check_exists])
    definition = TextAreaField(_('Definition'))
    entry_source = TextField(_('Entry source'))
    example = TextAreaField(_('Example'))
    explanation = TextAreaField(_('Explanation'))

    ps_choices = dropdown_list(PRODUCT_SUBSET, key=-1)
    product_subset = SelectField(_('Appears in'), choices=ps_choices,
        coerce=int)

    #
    # Linguistic fields
    #
    na_choices = dropdown_list(NORMATIVE_AUTHORIZATIONS)
    normative_authorization = SelectField(_('Normative authorization'),
                                          choices=na_choices)
    normative_authorization_org = SelectField(_('Organization'))

    # TODO: check if the passed terms exist in the DB
    subordinate_concept_generic = TextField(_('Hyponym'))
    superordinate_concept_generic = TextField(_('Hyperonym'))
    antonym_concept = TextField(_('Antonym'))
    related_concept = TextField()

    pos_choices = dropdown_list(PART_OF_SPEECH)
    part_of_speech = SelectField(_('Part of Speech'), choices=pos_choices)

    tt_choices = dropdown_list(TERM_TYPES)
    term_type = SelectField(_('Term type'), choices=tt_choices)


class AddTermForm(BaseTermForm):

    submit = SubmitField(_("Add"))


class EditTermForm(BaseTermForm):

    submit = SubmitField(_("Save changes"))
