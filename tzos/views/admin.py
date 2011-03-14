# -*- coding: utf-8 -*-
"""
    tzos.views.admin
    ~~~~~~~~~~~~~~~~

    Administration views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, g, redirect, render_template, request

from flaskext.babel import gettext as _

from tzos.extensions import db
from tzos.forms import AddUserPermissionForm
from tzos.helpers import url_for
from tzos.models import User
from tzos.permissions import admin as admin_permission

admin = Module(__name__)


@admin.route("/", methods=("GET", "POST"))
@admin_permission.require(401)
def settings():
    users = User.query.filter(User.role > User.MEMBER)

    addusersform = AddUserPermissionForm()
    addusersform.user.choices = [(u.id, u.username) for u in \
            User.query.filter(User.username!=g.user.username).all()]

    return render_template("admin/settings.html", users=users,
                                                  addusersform=addusersform)
