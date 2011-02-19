# -*- coding: utf-8 -*-
"""
    tzos.views.account
    ~~~~~~~~~~~~~~~~~~

    Authentication views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
import uuid

from flask import Module, abort, current_app, flash, g, redirect, \
    render_template, request, session

from flaskext.babel import gettext as _
from flaskext.mail import Message
from flaskext.principal import AnonymousIdentity, Identity, identity_changed

from tzos.extensions import db, mail
from tzos.forms import EditEmailForm, EditPasswordForm, EditProfileForm, \
    LoginForm, RecoverPasswordForm, ResetPasswordForm, SignupForm
from tzos.helpers import url_for
from tzos.models import User
from tzos.permissions import auth

account = Module(__name__)

@account.route('/register/', methods=('GET', 'POST'))
def register():
    form = SignupForm()

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))

        flash(_("Welcome, %(name)s.", name=user.username), "success")

        next_url = form.next.data

        if not next_url or next_url == request.path:
            next_url = url_for('frontend.index')

        return redirect(next_url)

    return render_template('account/register.html', form=form)


@account.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm(next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = \
            User.query.authenticate(form.login.data,
                                    form.password.data)

        if user and authenticated:
            session.permanent = form.remember.data

            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('frontend.index')

            return redirect(next_url)
        else:
            flash(_('Wrong username or password.'), 'error')

    return render_template('account/login.html', form=form)


@account.route("/logout/")
def logout():
    flash(_("You are now logged out."), "success")

    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('frontend.index'))


@account.route("/forgotpass/", methods=("GET", "POST"))
def forgot_password():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash(_("Please check your email for instructions on "
                  "how to access your account."), "success")

            user.activation_key = str(uuid.uuid4())
            db.session.commit()

            body = render_template("emails/recover_password.html",
                                   user=user)

            message = Message(subject=_("Recover your password"),
                              body=body,
                              recipients=[user.email])
            mail.send(message)

            return redirect(url_for("frontend.index"))
        else:
            flash(_("Sorry, no user found for that email address."), "error")

    return render_template("account/recover_password.html", form=form)


@account.route("/changepass/", methods=("GET", "POST"))
def change_password():
    user = None

    if g.user:
        user = g.user

    elif 'activation_key' in request.values:
        user = User.query.filter_by(
            activation_key=request.values['activation_key']).first()

    if user is None:
        abort(403)

    form = ResetPasswordForm(activation_key=user.activation_key)

    if form.validate_on_submit():
        user.password = form.password.data
        user.activation_key = None

        db.session.commit()

        flash(_("Your password has been changed, "
                "please log in again."), "success")

        # TODO: if user is already authenticated redirect it to its account page
        return redirect(url_for("account.login"))

    return render_template("account/change_password.html", form=form)


@account.route("/account/", methods=("GET", "POST"))
@auth.require(401)
def settings():
    profileform = EditProfileForm(obj=g.user)
    emailform = EditEmailForm(obj=g.user)
    passwordform = EditPasswordForm()

    allowed_actions = {
        'editpassword': passwordform,
        'editemail': emailform,
        'editprofile': profileform,
        }
    action = request.args.get('action', None)

    form = None
    if action and action in allowed_actions:
        form = allowed_actions[action]

    if form and form.validate_on_submit():
        form.populate_obj(g.user)
        db.session.commit()

        flash(_("Your account has been updated."), "success")

        return redirect(url_for("account.settings"))

    return render_template("account/settings.html", profileform=profileform,
                                                    emailform=emailform,
                                                    passwordform=passwordform)
