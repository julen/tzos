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

from tzos.extensions import cache, dbxml
from tzos.forms import SearchForm
from tzos.helpers import anon_cached, dropdown_list, get_dict_langs
from tzos.models import Comment, TermChange

frontend = Module(__name__)

@frontend.route('/')
@anon_cached()
def index():
    form = SearchForm()
    form.lang.choices = dropdown_list(get_dict_langs(), 'all', _(u'All'))

    latest_comments = cache.get("latest_comments")

    if latest_comments is None:
        latest_comments = Comment.query. \
                order_by(Comment.date_created.desc())[0:5]

        cache.set("latest_comments", latest_comments)

    latest_activity = cache.get("latest_activity")

    if latest_activity is None:
        qs = '''
        import module namespace term = "http://tzos.net/term" at "term.xqm";
        let $txs :=
            for $tx in collection($collection)//tig/transacGrp
            let $tig := $tx/..
            where term:is_public($tig)
            order by $tx/date descending
            return $tx
        for $tx in subsequence($txs, 1, 5)
        return term:activity($tx)
        '''

        latest_activity = dbxml.session. \
                raw_query(qs).as_callback(TermChange.parse).all()

        cache.set("latest_activity", latest_activity)

    return render_template('index.html', form=form,
                                         latest_activity=latest_activity,
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
