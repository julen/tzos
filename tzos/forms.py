# -*- coding: utf-8 -*-
"""
    tzos.forms
    ~~~~~~~~~~

    Form definitions.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import gettext, lazy_gettext as _
from flaskext.wtf import BooleanField, Form, HiddenField, Optional, \
    PasswordField, RecaptchaField, SubmitField, TextField, URL, email, \
    equal_to, regexp, required

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
    email = TextField("Your email address", validators=[
                      email(message=_("A valid email address is required."))])

    submit = SubmitField(_("Recover password"))


class BasePasswordForm(Form):
    password = PasswordField("Password", validators=[
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
