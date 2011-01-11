# -*- coding: utf-8 -*-
"""
    tzos.views.auth
    ~~~~~~~~~~~~~~~

    Authentication views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, redirect, render_template, session, url_for

from flaskext.babel import gettext as _

from tzos.extensions import db
from tzos.forms import LoginForm, SignupForm
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

        flash(_("Welcome, %(name)s", name=user.username), "success")

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

            flash(_("Welcome, %(name)s", name=user.username), "success")

            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('frontend.index')

            return redirect(next_url)
        else:
            flash('Wrong username or password', 'error')

    return render_template('auth/login.html', form=form)
