# -*- coding: utf-8 -*-
"""
    tzos.views.auth
    ~~~~~~~~~~~~~~~

    Authentication views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, current_app, redirect, render_template,\
                  session

from flaskext.babel import gettext as _
from flaskext.principal import AnonymousIdentity, Identity, identity_changed

from tzos.extensions import db
from tzos.forms import LoginForm, SignupForm
from tzos.helpers import url_for
from tzos.models import User

auth = Module(__name__)

@auth.route('/register/', methods=('GET', 'POST'))
def register():
    form = SignupForm()

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))

        flash(_("Welcome, %(name)s.", name=user.username), "success")

        next_url = form.next.data

        if not next_url or next_url == request.path:
            next_url = url_for('frontend.index')

        return redirect(next_url)

    return render_template('auth/register.html', form=form)


@auth.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user, authenticated = \
            User.query.authenticate(form.login.data,
                                    form.password.data)

        if user and authenticated:
            session.permanent = form.remember.data

            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('frontend.index')

            return redirect(next_url)
        else:
            flash('Wrong username or password.', 'error')

    return render_template('auth/login.html', form=form)


@auth.route("/logout/")
def logout():
    flash(_("You are now logged out."), "success")

    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('frontend.index'))
