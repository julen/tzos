# -*- coding: utf-8 -*-
"""
    tzos.views.frontend
    ~~~~~~~~~~~~~~~~~~~

    Fronted views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, redirect, render_template, request

from flaskext.babel import gettext as _

from tzos.helpers import url_for

from babel import Locale

frontend = Module(__name__)

@frontend.route('/<lang>/')
@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/<lang>/dict/')
def dict():
    newdict = request.args.get('setdict', None)

    if newdict:
        # FIXME: maybe a helper function could get locale display names
        flash(_(u"From now on your dictionary language is ‘%(dictname)s’.",
                dictname=Locale.parse(newdict).display_name.capitalize()))

        return redirect(url_for('frontend.index'))

    return render_template('dict.html')
