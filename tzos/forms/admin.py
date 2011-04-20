# -*- coding: utf-8 -*-
"""
    tzos.forms.admin
    ~~~~~~~~~~~~~~~~

    Admin forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import Form, SelectField, SubmitField

from tzos.helpers import get_all_langs
from tzos.models import User

class ModifyUserPermissionForm(Form):
    user = SelectField(_("Username"), coerce=int)

    role_choices = [(role, User.role_map[role]) \
        for role in sorted(User.role_map.keys())]
    role = SelectField(_("Role"), choices=role_choices, coerce=int)

    submit = SubmitField(_("Modify permissions"))


class AddLanguagesForm(Form):
    language_choices = get_all_langs()
    language = SelectField(_("Language"), choices=language_choices)

    submit = SubmitField(_("Add language"))
