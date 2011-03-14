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
from tzos.forms import ModifyUserPermissionForm
from tzos.helpers import url_for
from tzos.models import User
from tzos.permissions import admin as admin_permission

admin = Module(__name__)


@admin.route('/')
@admin_permission.require(401)
def settings():
    users = User.query.filter(User.role > User.MEMBER) \
                      .order_by('-role', 'username')

    usersform = ModifyUserPermissionForm()
    usersform.user.choices = [(u.id, u.username) for u in \
        User.query.filter(User.username!=g.user.username)
                  .order_by('username')]

    return render_template("admin/settings.html", users=users,
                                                  usersform=usersform)

@admin.route('/users/', methods=('POST',))
@admin_permission.require(401)
def users():
    form = ModifyUserPermissionForm()
    form.user.choices = [(u.id, u.username) for u in \
        User.query.filter(User.username!=g.user.username)]

    if form and form.validate_on_submit():
        user = User.query.filter_by(id=form.user.data).first_or_404()

        user.role = form.role.data
        db.session.commit()

        flash(_(u"Permissions for ‘%(user)s’ have been updated.",
                user=user.username), "success")
    else:
        flash(_("Error while updating permissions."), "error")

    return redirect(url_for("admin.settings"))
