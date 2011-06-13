# -*- coding: utf-8 -*-
"""
    tzos.forms.account
    ~~~~~~~~~~~~~~~~~~

    Account forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import gettext, lazy_gettext as _
from flaskext.wtf import BooleanField, Form, HiddenField, Optional, \
    PasswordField, RecaptchaField, SubmitField, TextField, URL, \
    ValidationError, email, equal_to, regexp, required

from tzos.models import User

USERNAME_RE = r'^[\w.+-]+$'

is_username = regexp(USERNAME_RE,
                     message=_(u"You can only use letters, numbers or dashes"))


class LoginForm(Form):
    next = HiddenField()

    login = TextField(_(u'Username or email address'), validators=[
                      required(message=\
                               _(u'You must provide an email or username.'))])

    password = PasswordField(_(u'Password'))

    remember = BooleanField(_(u'Remember me'))

    submit = SubmitField(_(u'Login'))


class SignupForm(Form):
    next = HiddenField()

    username = TextField(_(u"Username"), validators=[
                         required(message=_(u"Username is required.")),
                         is_username])

    password = PasswordField(_(u"Password"), validators=[
                             required(message=_(u"Password is required."))])

    password_repeat = PasswordField(_(u"Repeat Password"), validators=[
                                    equal_to("password", message=\
                                             _(u"Passwords don't match"))])

    email = TextField(_(u"Email address"), validators=[
                      required(message=_(u"Email address is required.")),
                      email(message=_(u"A valid email address is required."))])

    recaptcha = RecaptchaField(_(u"Copy the words appearing below"))

    submit = SubmitField(_(u"Signup"))


    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError, gettext(u"This username is taken.")

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()
        if user:
            raise ValidationError, gettext(u"This email is taken.")


class RecoverPasswordForm(Form):
    email = TextField(_(u"Your email address"), validators=[
                      email(message=_(u"A valid email address is required."))])

    submit = SubmitField(_(u"Recover password"))


class BasePasswordForm(Form):
    password = PasswordField(_(u"Password"), validators=[
                             required(message=_(u"Password is required."))])

    password_again = PasswordField(_(u"Repeat password"), validators=[
                                   equal_to("password", message=\
                                            _(u"Passwords don't match."))])

class ResetPasswordForm(BasePasswordForm):
    activation_key = HiddenField()

    submit = SubmitField(_(u"Reset password"))


class EditPasswordForm(BasePasswordForm):
    submit = SubmitField(_(u"Change password"))


class EditEmailForm(Form):
    email = TextField(_(u"Your email address"), validators=[
                      required(message=_(u"Email address required.")),
                      email(message=_(u"A valid email address is required."))])

    submit = SubmitField(_(u"Edit email address"))

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()

        if user:
            raise ValidationError, gettext(u"This email is taken.")


class EditProfileForm(Form):
    display_name = TextField(_(u"Display name"))

    website = TextField(_(u"Website"), validators=[
                        Optional(),
                        URL(message=_(u"The URL must be valid."))])

    company = TextField(_(u"Company/Organization"))

    location = TextField(_(u"Location"))

    submit = SubmitField(_(u"Update information"))

