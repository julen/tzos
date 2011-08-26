# -*- coding: utf-8 -*-
"""
    tzos.views.frontend
    ~~~~~~~~~~~~~~~~~~~

    Frontend views.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Module, flash, g, redirect, render_template, request, url_for

from flaskext.babel import gettext as _
from flaskext.mail import Message

from tzos.extensions import cache, dbxml, mail
from tzos.forms import ContactForm, SearchForm
from tzos.helpers import get_dict_langs
from tzos.models import Comment, TermChange, User

frontend = Module(__name__)

@frontend.route('/')
def index():

    form = SearchForm()
    form.lang.choices = get_dict_langs()

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
            for $tx in collection($collection)/martif/text/body/termEntry/langSet/tig/transacGrp
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
        flash(_(u"From now on your dictionary language is ‘%(dictname)s’.",
                dictname=newdict))

        return redirect(url_for('frontend.index'))

    return render_template('dict.html')

@frontend.route('/contact/', methods=('GET', 'POST',))
def contact():

    if g.user:
        form = ContactForm(obj=g.user)
    else:
        form = ContactForm()

    if form and form.validate_on_submit():

        admins = User.query.filter(User.role == User.ADMIN)
        admin_emails = [admin.email for admin in admins]

        body = render_template("emails/contact.html",
                               name=form.display_name.data,
                               email=form.email.data,
                               text=form.text.data)

        message = Message(subject=_(u"TZOS: Contact from website"),
                          body=body,
                          recipients=admin_emails)
        mail.send(message)

        flash(_(u"Thanks for your message. We will try to reply you "
                "back as fast as possible."), "success")

        return redirect(url_for("frontend.index"))

    return render_template('contact.html', contact_form=form)
