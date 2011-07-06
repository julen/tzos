# -*- coding: utf-8 -*-
"""
    tzos.forms.frontend
    ~~~~~~~~~~~~~~~~~~~

    Frontend forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import email, Form, RecaptchaField, SubmitField, \
        TextAreaField, TextField, required

class ContactForm(Form):

    display_name = TextField(_(u"Full name"), validators=[
        required(message=_("Full name is required."))])

    email = TextField(_(u"Email address"), validators=[
        required(message=_("Email address is required.")),
        email(message=_("A valid email address is required."))])

    text = TextAreaField(_(u"Write here"), validators=[
        required(message=_("Text is required."))])

    recaptcha = RecaptchaField(_(u"Copy the words appearing below"))

    submit = SubmitField(_(u"Send"))
