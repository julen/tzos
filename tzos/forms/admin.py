# -*- coding: utf-8 -*-
"""
    tzos.forms.admin
    ~~~~~~~~~~~~~~~~

    Admin forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import Form, Length, SelectField, SubmitField, TextField, \
        required

from tzos.models import User

class ModifyUserPermissionForm(Form):
    user = SelectField(_("Username"), coerce=int)

    role_choices = [(role, User.role_map[role]) \
        for role in sorted(User.role_map.keys())]
    role = SelectField(_("Role"), choices=role_choices, coerce=int)

    submit = SubmitField(_("Modify permissions"))


class AddLanguagesForm(Form):

    name_desc = _("Original language name as it should be displayed "
                  "on the interface.")
    name = TextField(_("Language name"), description=name_desc,
            validators=[required(message=_("Language name is required."))])

    code = TextField(_("Language code"), validators=[
        Length(min=2, max=2,
               message=_("Language code must be exactly two characters length.")),
        required(message=_("Language code is required."))
        ])

    submit = SubmitField(_("Add language"))
