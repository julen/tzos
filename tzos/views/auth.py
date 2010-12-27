# -*- coding: utf-8 -*-
"""
    tzos.views.auth
    ~~~~~~~~~~~~~~

    Authentication views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, render_template

auth = Module(__name__)

@auth.route('/register')
def register():
    return render_template('auth/register.html')

@auth.route('/login')
def login():
    return render_template('auth/login.html')
