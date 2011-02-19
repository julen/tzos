# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, flash, g, redirect, render_template, request, session

from flaskext.babel import Babel, gettext as _, format_date
from flaskext.principal import Principal, identity_loaded

from babel import Locale

from tzos import views
from tzos.extensions import db, dbxml, mail
from tzos.helpers import url_for
from tzos.models import User

__all__ = ["create_app"]

MODULES = (
    (views.frontend, ''),
    (views.account, '/<lang>'),
    (views.search, '/<lang>/search'),
    (views.terms, '/<lang>/terms'),
    (views.user, '/<lang>/user'),
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
        newdict = request.args.get('setdict', None)

        if newdict:
            session['tzos_dict'] = newdict
        elif not 'tzos_dict' in session:
            session['tzos_dict'] = app.config['TZOS_DEFAULT_DICT']

    @app.before_request
    def set_lang():
        if request.endpoint != 'static':
            lang = None
            goto = False

            # First try to determine the language from the URL
            if request.view_args and 'lang' in request.view_args:
                # Pop the lang from the attributes passed to the view function
                lang = request.view_args.pop('lang', None)

                if lang not in app.available_languages:
                    lang = None
                    goto = True

            # No lang set in the URL, let's try other ways
            if lang is None:
                # First alternative: picking language from Accept-Lang headers
                accept_languages = app.config.get('ACCEPT_LANGUAGES',
                                                  app.available_languages)
                lang = request.accept_languages.best_match(accept_languages)

                if request.endpoint == 'frontend.index':
                    goto = True

                # Second alternative: get the default from the config file
                if lang is None:
                    lang = app.config.get('BABEL_DEFAULT_LOCALE', 'en')

            g.lang = lang

            if goto:
                return redirect(url_for('frontend.index'))


def configure_jinja(app):
    app.jinja_env.globals.update(url_for=url_for)

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
        # TODO: cache items not to hit the disk each time we run this
        dicts = []

        qs = "distinct-values(collection('{0}')/martif/text/body/termEntry/langSet/@xml:lang)".format(g.dbxml.collection)
        dictlist = g.dbxml.raw_query(qs).as_str().all()

        for d in dictlist:
            l = Locale.parse(d)
            dicts.append((l.language, l.display_name))

        return dict(tzos_dicts=dicts)


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
        return g.lang
