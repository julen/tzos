# -*- coding: utf-8 -*-

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.cfg')

    from tzos.views.frontend import frontend
    app.register_module(frontend)

    from tzos.views.auth import auth
    app.register_module(auth)

    return app
