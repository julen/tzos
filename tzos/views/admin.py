# -*- coding: utf-8 -*-
"""
    tzos.views.admin
    ~~~~~~~~~~~~~~~~

    Administration views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, g, redirect, render_template, request, url_for

from flaskext.babel import gettext as _

from tzos.extensions import db
from tzos.forms import AddLanguagesForm, AddTermOriginForm, \
        EditTermOriginForm, ModifyUserPermissionForm
from tzos.models import TermOrigin, User
from tzos.permissions import admin as admin_permission

admin = Module(__name__)


@admin.route('/')
@admin_permission.require(401)
def settings():
    users = User.query.filter(User.role > User.MEMBER) \
                      .order_by('-role', 'username')

    users_form = ModifyUserPermissionForm()
    users_form.user.choices = [(u.id, u.username) for u in \
        User.query.filter(User.username!=g.user.username)
                  .order_by('username')]

    langs_form = AddLanguagesForm()

    origin_choices = TermOrigin.query.values(TermOrigin.id, TermOrigin.name)
    origins_form = AddTermOriginForm()
    origins_form.parent_id.choices = origin_choices

    return render_template("admin/settings.html", users=users,
                                                  users_form=users_form,
                                                  langs_form=langs_form,
                                                  origins_form=origins_form)

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

@admin.route('/origin/add/', methods=('POST',))
@admin_permission.require(401)
def add_origin():
    origin_choices = TermOrigin.query.values(TermOrigin.id, TermOrigin.name)
    form = AddTermOriginForm()
    form.parent_id.choices = origin_choices

    if form and form.validate_on_submit():
        origin = TermOrigin()
        form.populate_obj(origin)

        db.session.add(origin)
        db.session.commit()

        flash(_(u"Term origin ‘%(origin)s’ has been added.",
                origin=origin.name), "success")
    else:
        flash(_("Error while adding term origin."), "error")

    return redirect(url_for("admin.settings"))
