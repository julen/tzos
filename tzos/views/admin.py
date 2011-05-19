# -*- coding: utf-8 -*-
"""
    tzos.views.admin
    ~~~~~~~~~~~~~~~~

    Administration views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Markup, Module, flash, g, redirect, render_template, \
        request, url_for

from flaskext.babel import gettext as _

from tzos.extensions import db
from tzos.forms import AddLanguagesForm, AddTermOriginForm, \
        EditTermOriginForm, ModifyUserPermissionForm
from tzos.helpers import dropdown_list
from tzos.models import TermOrigin, User
from tzos.permissions import admin as admin_permission

admin = Module(__name__)


def gen_users_form():

    form = ModifyUserPermissionForm()
    form.user.choices = [(u.id, u.username) for u in \
        User.query.filter(User.username!=g.user.username)
                  .order_by('username')]

    return form


def gen_origins_dropdown():

    def _get_children(parent_id, depth):

        for origin in origins:

            if origin.parent_id == parent_id:
                name = Markup((u'&nbsp;' * 3) * depth + origin.name).unescape()
                dropdown.append((origin.id, name))

                if origin.children:
                    _get_children(origin.id, depth + 1)

    dropdown = []
    origins = TermOrigin.query.order_by('name').all()
    parents = [(o.id, o.name) for o in origins if o.parent_id is None]

    for id, name in parents:
        dropdown.append((id, name))
        _get_children(id, 1)

    return dropdown


def gen_add_origins_form():

    form = AddTermOriginForm()

    origins = gen_origins_dropdown()
    form.parent_id.choices = dropdown_list(origins, key=-1, value='')

    return form


@admin.route('/')
@admin_permission.require(401)
def settings():

    users = User.query.filter(User.role > User.MEMBER) \
                      .order_by('-role', 'username')

    users_form = gen_users_form()
    langs_form = AddLanguagesForm()
    origins_form = gen_add_origins_form()

    return render_template("admin/settings.html", users=users,
                                                  users_form=users_form,
                                                  langs_form=langs_form,
                                                  origins_form=origins_form)

@admin.route('/users/', methods=('POST',))
@admin_permission.require(401)
def users():

    form = users_form()

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

    form = gen_add_origins_form()

    if form and form.validate_on_submit():
        origin = TermOrigin(name=form.name.data)

        if form.parent_id.data > -1:
            origin.parent_id = form.parent_id.data

        db.session.add(origin)
        db.session.commit()

        flash(_(u"Term origin ‘%(origin)s’ has been added.",
                origin=origin.name), "success")
    else:
        flash(_("Error while adding term origin."), "error")

    return redirect(url_for("admin.settings"))
