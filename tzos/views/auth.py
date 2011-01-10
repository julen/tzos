# -*- coding: utf-8 -*-
"""
    tzos.views.auth
    ~~~~~~~~~~~~~~~

    Authentication views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import flash, Module, render_template

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
        flash('Data is OK', 'success')

    return render_template('auth/login.html', form=form)
