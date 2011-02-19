# -*- coding: utf-8 -*-
"""
    tzos.views.user
    ~~~~~~~~~~~~~~~

    User profile views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, render_template

from tzos.models import User

user = Module(__name__)

@user.route('/<username>/')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user/profile.html', user=user)
