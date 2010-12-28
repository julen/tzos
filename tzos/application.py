# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, request

from flaskext.babel import Babel

from tzos import views

__all__ = ["create_app"]

MODULES = (
    (views.frontend, ''),
    (views.auth, ''),
)

def create_app(config):
    app = Flask(__name__)

    configure_app(app, config)

    configure_modules(app)
    configure_i18n(app)

    return app


def configure_app(app, config):
    app.config.from_pyfile(config)
    app.config.from_envvar('TZOS_CONFIG', silent=True)

def configure_modules(app):
    for module, url_prefix in MODULES:
        app.register_module(module, url_prefix=url_prefix)

def configure_i18n(app):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES',
                                          ['eu', 'es', 'es-ES', 'en'])

        return request.accept_languages.best_match(accept_languages)
