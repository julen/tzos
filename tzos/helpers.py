# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~

    Helper functions

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import _request_ctx_stack, g

def url_for(endpoint, **values):
    """Overriden method to always add the language information."""

    # If no lang is passed, add it between the values
    if endpoint != 'static':
        if not 'lang' in values:
            values['lang'] = g.lang

    # The code below is from flask.url_for
    ctx = _request_ctx_stack.top
    if '.' not in endpoint:
        mod = ctx.request.module
        if mod is not None:
            endpoint = mod + '.' + endpoint
    elif endpoint.startswith('.'):
        endpoint = endpoint[1:]
    external = values.pop('_external', False)
    return ctx.url_adapter.build(endpoint, values, force_external=external)
