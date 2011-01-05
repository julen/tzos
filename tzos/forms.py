# -*- coding: utf-8 -*-
"""
    tzos.forms
    ~~~~~~~~~~

    Form definitions.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _ 
from flaskext.wtf import BooleanField, Form, HiddenField, PasswordField, required, SubmitField, TextField

class SearchForm(Form):
    search_text = TextField(_('Search terms'), validators=[required()])

    submit = SubmitField(_('Search'))


class LoginForm(Form):
    next = HiddenField()
    
    remember = BooleanField(_('Remember me'))
    login = TextField(_('Username or email address'), validators=[
                      required(message=\
                               _('You must provide an email or username'))])
    password = PasswordField(_('Password'))

    submit = SubmitField(_('Login'))
