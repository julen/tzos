# -*- coding: utf-8 -*-
"""
    tzos.forms.admin
    ~~~~~~~~~~~~~~~~

    Admin forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _
from flaskext.wtf import Form, IntegerField, Length, SelectField, SubmitField, \
        TextField, required

from tzos.forms.fields import SelectFieldPlus
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


class BaseTermOriginForm(Form):

    name = TextField(_(u"Name"),
            validators=[required(message=_(u"Name is required."))])

    parent_id = SelectFieldPlus(coerce=int, placeholder=-1)

class AddTermOriginForm(BaseTermOriginForm):

    submit = SubmitField(_(u"Create"))

class EditTermOriginForm(BaseTermOriginForm):

    submit = SubmitField(_(u"Edit"))


class BaseTermSourceForm(Form):

    name = TextField(_(u"Name"),
            validators=[required(message=_(u"Name is required."))])


class AddTermSourceForm(BaseTermSourceForm):

    submit = SubmitField(_(u"Create"))


class EditTermSourceForm(BaseTermSourceForm):

    submit = SubmitField(_(u"Edit"))


class BaseTermSubjectForm(Form):

    code = IntegerField(_(u"Code"))

    parent_id = SelectFieldPlus(_(u"Parent"), coerce=int, placeholder=-1)


class AddTermSubjectForm(BaseTermSubjectForm):

    submit = SubmitField(_(u"Add"))


class EditTermSubjectForm(BaseTermSubjectForm):

    submit = SubmitField(_(u"Edit"))


class ExportForm(Form):

    submit = SubmitField(_(u"Export"))


class BackupForm(Form):

    submit = SubmitField(_(u"Make backup"))


class DeleteUploadForm(Form):

    submit = SubmitField(_(u"Delete uploaded terms"))
