# -*- coding: utf-8 -*-
"""
    tzos.views.auth
    ~~~~~~~~~~~~~~

    Authentication views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import flash, Module, render_template

from tzos.forms import LoginForm

auth = Module(__name__)

@auth.route('/register/')
def register():
    return render_template('auth/register.html')


@auth.route('/login/', methods=('GET', 'POST'))
def login():

    form = LoginForm()

    if form.validate_on_submit():
        flash('Data is OK', 'success')
    else:
        flash('Data is NOT OK', 'error')

    return render_template('auth/login.html', form=form)
