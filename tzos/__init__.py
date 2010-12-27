# -*- coding: utf-8 -*-

from flask import Flask

def create_app():
    app = Flask(__name__)

    from tzos.views.frontend import frontend
    app.register_module(frontend)

    return app
