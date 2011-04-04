# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~

    Helper functions

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import _request_ctx_stack, abort, current_app, g, request

from babel import Locale
from functools import wraps

from tzos.extensions import dbxml


def url_for(endpoint, **values):
    """Overriden method to always add the language information."""

    # If no lang is passed, add it between the values
    if endpoint != '.static':
        if not 'lang' in values:
            values['lang'] = g.ui_lang
        else:
            # This is useful for URLs used for choosing languages
            values.update(request.view_args)

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


def get_tzos_dicts(only_codes=False):
    """Returns a list with tuples of all the available dictionaries.
    The tuple elements are language codes and language names.

    :param only_codes: if set to True, returns a list of language codes.
                       Defaults to False.
    """
    # TODO: cache items not to hit the disk each time we run this
    dicts = []

    qs = "distinct-values(collection('{0}')//langSet/@xml:lang)". \
            format(dbxml.get_db().collection)
    dictlist = dbxml.get_db().raw_query(qs).as_str().all()

    for d in dictlist:
        l = Locale.parse(d)
        locale = l.language if only_codes else (l.language, l.display_name)
        dicts.append(locale)

    return dicts


def require_valid_dict(f):
    """A decorator that checks whether the dictionary passed in the URL exists
    in the database or not. If not, aborts the request with 404."""

    @wraps(f)
    def decorator(dict, *args, **kwargs):
        available_dicts = get_tzos_dicts(only_codes=True)

        if dict not in available_dicts:
            return abort(404)

        return f(dict, *args, **kwargs)

    return decorator
