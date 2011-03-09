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
#from tzos.forms import EditPermissionsForm
from tzos.helpers import url_for
from tzos.permissions import admin as admin_permission

admin = Module(__name__)


@admin.route("/", methods=("GET", "POST"))
@admin_permission.require(401)
def settings():
    #permissionform = EditPermissionForm(obj=g.user)

    allowed_actions = {
        #'editpermission': permissionform,
        }
    action = request.args.get('action', None)

    form = None
    if action and action in allowed_actions:
        form = allowed_actions[action]

    if form and form.validate_on_submit():
        form.populate_obj(g.user)
        db.session.commit()

        flash(_("Your account has been updated."), "success")

        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html")
                           #permissionform=permissionform)
