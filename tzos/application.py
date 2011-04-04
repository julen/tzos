# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, flash, g, redirect, render_template, request, \
    session, url_for

from flaskext.assets import Bundle, Environment
from flaskext.babel import Babel, gettext as _, format_date
from flaskext.principal import Principal, identity_loaded

from tzos import views
from tzos.extensions import db, dbxml, mail
from tzos.helpers import get_dict_langs, url_for2
from tzos.models import User

__all__ = ["create_app"]

MODULES = (
    (views.frontend, ''),
    (views.account, ''),
    (views.admin, '/admin'),
    (views.search, '/search'),
    (views.glossary, '/glossary'),
    (views.terms, '/term'),
    (views.user, '/user'),
)

def create_app(config=None):
    app = Flask(__name__)

    configure_app(app, config)

    configure_errorhandlers(app)
    configure_extensions(app)
    configure_before_handlers(app)
    configure_modules(app)
    configure_jinja(app)
    configure_context_processors(app)

    return app


def configure_app(app, config):
    if config is not None:
        app.config.from_pyfile(config)

    app.config.from_envvar('TZOS_CONFIG', silent=True)


def configure_modules(app):
    for module, url_prefix in MODULES:
        app.register_module(module, url_prefix=url_prefix)


def configure_extensions(app):
    mail.init_app(app)

    configure_assets(app)
    configure_databases(app)
    configure_i18n(app)
    configure_identity(app)


def configure_errorhandlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html")

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html")

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html")

    @app.errorhandler(401)
    def unauthorized(e):
        flash(_("You must login to see this page."), "error")
        return redirect(url_for("account.login", next=request.path))


def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)

    @app.before_request
    def set_dict():
        new_dict = request.args.get('setdict', None)

        if new_dict:
            session['dict_lang'] = new_dict

            # Set a new dict while in the glossary, refresh the current page
            # but with the newly selected dictionary
            if request.endpoint == 'glossary.list_letter':
                old_dict = request.view_args['dict']

                if new_dict != old_dict:
                    request.view_args.update({'dict': new_dict})

                    return redirect(url_for(request.endpoint,
                                            **request.view_args))

        elif not 'dict_lang' in session:
            session['dict_lang'] = app.config['TZOS_DEFAULT_DICT_LANG']

    @app.before_request
    def set_lang():
        lang = None
        new_ui_lang = request.args.get('setuilang', None)

        # If language is passed explicitely, try to set it
        if new_ui_lang or new_ui_lang in app.available_languages:
            g.ui_lang = new_ui_lang
        else:
            # Try to pick the language from the Accept-Lang headers
            accept_languages = app.config.get('ACCEPT_LANGUAGES',
                                              app.available_languages)
            lang = request.accept_languages.best_match(accept_languages)

            # As a last option, get the default from the config file
            if lang is None:
                lang = app.config.get('BABEL_DEFAULT_LOCALE')

            g.ui_lang = lang


def configure_jinja(app):
    app.jinja_env.globals.update(url_for2=url_for2)

    @app.template_filter()
    def dateformat(value, format):
        return format_date(value, format=format)


def configure_context_processors(app):

    @app.context_processor
    def get_langs():
        # TODO: cache items not to hit the disk each time we run this
        langs = []
        langlist = app.babel_instance.list_translations()

        for l in langlist:
            langs.append((l.language, l.display_name))

        return dict(langs=langs)

    @app.context_processor
    def get_dicts():
        return dict(dict_langs=get_dict_langs())


def configure_assets(app):
    assets = Environment(app)

    js = Bundle('tzos.js', 'tabs.js',
                filters='jsmin', output='tzos-packed.js')

    assets.register('js_all', js)


def configure_databases(app):
    db.init_app(app)
    dbxml.init_app(app)


def configure_identity(app):
    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)


def configure_i18n(app):
    babel = Babel(app)

    app.available_languages = [l.language for l in babel.list_translations()]

    @babel.localeselector
    def get_locale():
        return g.ui_lang
