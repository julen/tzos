# -*- coding: utf-8 -*-
"""
    tzos.permissions
    ~~~~~~~~~~~~~~~~

    Identity permissions

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.principal import RoleNeed, Permission

admin = Permission(RoleNeed('admin'))
moderator = Permission(RoleNeed('moderator'))
corrector = Permission(RoleNeed('corrector'))
auth = Permission(RoleNeed('authenticated'))
