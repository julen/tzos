# -*- coding: utf-8 -*-
"""
    tzos.forms
    ~~~~~~~~~~

    Form definitions.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import gettext, lazy_gettext as _
from flaskext.wtf import AnyOf, BooleanField, Form, HiddenField, Optional, \
    PasswordField, RecaptchaField, SelectField, SubmitField, TextAreaField, \
    TextField, URL, ValidationError, email, equal_to, regexp, required

from tzos.extensions import dbxml
from tzos.models import User

USERNAME_RE = r'^[\w.+-]+$'

is_username = regexp(USERNAME_RE,
                     message=_("You can only use letters, numbers or dashes"))

class SearchForm(Form):
    term = TextField(_('Search terms'))
    source = TextField(_('Source'))
    example = TextField(_('Examples'))
    definition = TextField(_('Definition'))
    sample = TextField(_('Sample text'))

    submit = SubmitField(_('Search'))


class LoginForm(Form):
    next = HiddenField()

    login = TextField(_('Username or email address'), validators=[
                      required(message=\
                               _('You must provide an email or username.'))])

    password = PasswordField(_('Password'))

    remember = BooleanField(_('Remember me'))

    submit = SubmitField(_('Login'))


class SignupForm(Form):
    next = HiddenField()

    username = TextField(_("Username"), validators=[
                         required(message=_("Username is required.")),
                         is_username])

    password = PasswordField(_("Password"), validators=[
                             required(message=_("Password is required."))])

    password_repeat = PasswordField(_("Repeat Password"), validators=[
                                    equal_to("password", message=\
                                             _("Passwords don't match"))])

    email = TextField(_("Email address"), validators=[
                      required(message=_("Email address is required.")),
                      email(message=_("A valid email address is required."))])

    recaptcha = RecaptchaField(_("Copy the words appearing below"))

    submit = SubmitField(_("Signup"))


class RecoverPasswordForm(Form):
    email = TextField(_("Your email address"), validators=[
                      email(message=_("A valid email address is required."))])

    submit = SubmitField(_("Recover password"))


class BasePasswordForm(Form):
    password = PasswordField(_("Password"), validators=[
                             required(message=_("Password is required."))])

    password_again = PasswordField(_("Repeat password"), validators=[
                                   equal_to("password", message=\
                                            _("Passwords don't match."))])

class ResetPasswordForm(BasePasswordForm):
    activation_key = HiddenField()

    submit = SubmitField(_("Reset password"))


class EditPasswordForm(BasePasswordForm):
    submit = SubmitField(_("Change password"))


class EditEmailForm(Form):
    email = TextField(_("Your email address"), validators=[
                      required(message=_("Email address required.")),
                      email(message=_("A valid email address is required."))])

    submit = SubmitField(_("Edit email address"))

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()

        if user:
            raise ValidationError, gettext("This email is taken.")


class EditProfileForm(Form):
    display_name = TextField(_("Display name"))

    website = TextField(_("Website"), validators=[
                        Optional(),
                        URL(message=_("The URL must be valid."))])

    company = TextField(_("Company/Organization"))

    location = TextField(_("Location"))

    submit = SubmitField(_("Update information"))


class ModifyUserPermissionForm(Form):
    user = SelectField(_("Username"), coerce=int)

    role_choices = [(role, User.role_map[role]) \
        for role in sorted(User.role_map.keys())]
    role = SelectField(_("Role"), choices=role_choices, coerce=int)

    submit = SubmitField(_("Modify permissions"))


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
