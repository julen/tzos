# -*- coding: utf-8 -*-
"""
    tzos.forms.terms
    ~~~~~~~~~~~~~~~~

    Terms forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import AnyOf, BooleanField, Form, HiddenField, SelectField, \
    SubmitField, TextAreaField, TextField, ValidationError, required

from tzos.extensions import dbxml

class AddTermForm(Form):

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

    def check_exists(form, field):
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

    def check_not_mine(form, field):
        message = _("You must specify the author's name.")

        if form.not_mine.data and field.data == "":
            raise ValidationError(message)


    #
    # Core fields
    #

    term = TextField(_("Term"), validators=[
        required(message=_("Term is required.")),
        check_collision])

    language = SelectField(_("Language"), validators=[
        required(message=_("Language is required."))])


    concept_origin = TextField(_("Origin"), validators=[
        required(message=_("Origin is required."))])

    element_working_status = SelectField(_("Working status"), validators=[
        required(message=_("Working status is required."))])

    subject_field = TextField(_("Subject field"), validators=[
        required(message=_("Subject field is required."))])


    syntrans = BooleanField(_("This term is a synonym or a translation for another term."))

    syntrans_term = TextField(_("Term"), validators=[
        check_syntrans,
        check_exists])

    syntrans_lang = SelectField(_("Language"), validators=[
        required(message=_("Language is required."))])


    not_mine = BooleanField(_("The author of this term is another person."))
    originating_person = TextField(_("Originating person"), validators=[
        check_not_mine])

    #
    # Transaction-related stuff
    #
    transac_type = HiddenField(default='input', validators=[AnyOf('input')])

    #
    # Optional fields
    #
    context = TextAreaField()
    cross_reference = TextField()
    definition = TextAreaField()
    entry_source = TextField()
    example = TextAreaField()
    explanation = TextAreaField()
    product_subset = TextField()

    #
    # Linguistic fields
    #
    normative_authorization = TextField()
    part_of_speech = TextField()

    subordinate_concept_generic = TextField()
    superordinate_concept_generic = TextField()
    antonym_concept = TextField()
    related_concept = TextField()

    term_type = TextField()


    submit = SubmitField(_("Add"))
