# -*- coding: utf-8 -*-
"""
    tzos.forms
    ~~~~~~~~~~

    Forms module.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from .account import LoginForm, SignupForm, RecoverPasswordForm, \
        BasePasswordForm, ResetPasswordForm, EditPasswordForm, \
        EditEmailForm, EditProfileForm
from .admin import AddLanguagesForm, AddTermOriginForm, AddTermSourceForm, \
        EditTermOriginForm, EditTermSourceForm, ModifyUserPermissionForm
from .comments import CommentForm
from .search import SearchForm
from .terms import AddTermForm, AddTermFormCor, EditTermForm, \
        EditTermFormCor, EditTermFormMod, UploadForm, UploadFormCor
