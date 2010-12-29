# -*- coding: utf-8 -*-
"""
    tzos.views.frontend
    ~~~~~~~~~~~~~~

    Fronted views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import g, Module, render_template

frontend = Module(__name__)

@frontend.route('/<lang>/')
@frontend.route('/')
def index():
    return render_template('index.html')
