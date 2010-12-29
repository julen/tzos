# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import g, Flask, redirect, request
from flask.helpers import get_flashed_messages, _tojson_filter

from flaskext.babel import Babel

from tzos import views
from tzos.helpers import url_for

__all__ = ["create_app"]

MODULES = (
    (views.frontend, ''),
    (views.auth, '/<lang>'),
)

class TZOS(Flask):
    """Subclass application class."""

    def init_jinja_globals(self):
        """Overriden function to support custom url_for methods in templates."""
        self.jinja_env.globals.update(
            url_for=url_for,
            get_flashed_messages=get_flashed_messages
        )
        self.jinja_env.filters['tojson'] = _tojson_filter


def create_app(config):
    app = TZOS(__name__)

    configure_app(app, config)

    configure_before_handlers(app)
    configure_modules(app)
    configure_i18n(app)

    return app


def configure_app(app, config):
    app.config.from_pyfile(config)
    app.config.from_envvar('TZOS_CONFIG', silent=True)


def configure_modules(app):
    for module, url_prefix in MODULES:
        app.register_module(module, url_prefix=url_prefix)


def configure_before_handlers(app):
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


def configure_i18n(app):
    babel = Babel(app)

    app.available_languages = [l.language for l in babel.list_translations()]

    @babel.localeselector
    def get_locale():
        return g.lang
