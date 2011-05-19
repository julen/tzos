# -*- coding: utf-8 -*-
"""
    tzos.views.frontend
    ~~~~~~~~~~~~~~~~~~~

    Frontend views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, redirect, render_template, request, url_for

from flaskext.babel import gettext as _

from babel import Locale

from tzos.forms import SearchForm
from tzos.helpers import dropdown_list, get_dict_langs
from tzos.models import Comment

frontend = Module(__name__)

@frontend.route('/')
def index():
    form = SearchForm()
    form.lang.choices = dropdown_list(get_dict_langs(), 'all', _('All'))

    latest_comments = Comment.query.order_by(Comment.date_created.desc())[0:5]

    return render_template('index.html', form=form,
                                         latest_comments=latest_comments)

@frontend.route('/dict/')
def dict():
    newdict = request.args.get('setdict', None)

    if newdict:
        # FIXME: maybe a helper function could get locale display names
        flash(_(u"From now on your dictionary language is ‘%(dictname)s’.",
                dictname=Locale.parse(newdict).display_name.capitalize()))

        return redirect(url_for('frontend.index'))

    return render_template('dict.html')
