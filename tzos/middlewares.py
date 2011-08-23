# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~

    Middlewares for the WSGI app.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""

class PrefixMiddleware(object):

    def __init__(self, app, prefix='/'):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.prefix 
        return self.app(environ, start_response)
