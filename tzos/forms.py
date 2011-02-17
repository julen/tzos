# -*- coding: utf-8 -*-
"""
    tzos.forms
    ~~~~~~~~~~

    Form definitions.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import BooleanField, Form, HiddenField, PasswordField,\
                         RecaptchaField, SubmitField, TextField, email,\
                         equal_to, regexp, required

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

    remember = BooleanField(_('Remember me'))
    login = TextField(_('Username or email address'), validators=[
                      required(message=\
                               _('You must provide an email or username.'))])
    password = PasswordField(_('Password'))

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


class ChangePasswordForm(Form):
    activation_key = HiddenField()

    password = PasswordField("Password", validators=[
                             required(message=_("Password is required."))])

    password_again = PasswordField(_("Password again"), validators=[
                                   equal_to("password", message=\
                                            _("Passwords don't match."))])

    submit = SubmitField(_("Save"))
