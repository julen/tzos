# -*- coding: utf-8 -*-
"""
    tzos.views.user
    ~~~~~~~~~~~~~~~

    User profile views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, render_template

from tzos.extensions import dbxml
from tzos.models import Comment, TermChange, User

user = Module(__name__)

@user.route('/<username>/')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    user_comments = Comment.query.filter_by(author=user).order_by(Comment.date_created.desc())[0:5]

    qs = '''
    import module namespace term = "http://tzos.net/term" at "term.xqm";
    let $txs :=
        for $tx in collection($collection)//tig/transacGrp
        let $tig := $tx/..
        where term:is_public($tig) and
              $tx/transacNote[@type="responsibility"]/string()="{0}"
        order by $tx/date descending
        return term:activity($tig, $tx)
    return subsequence($txs, 1, 5)
    '''.format(username.encode('utf-8'))

    user_activity = \
            dbxml.session.raw_query(qs).as_callback(TermChange.parse).all()

    return render_template('user/profile.html', user=user,
                                                user_activity=user_activity,
                                                user_comments=user_comments)
