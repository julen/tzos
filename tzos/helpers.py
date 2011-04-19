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

import random
import string


def url_for2(endpoint, **values):
    """Overriden method to always add request.view_args."""

    if endpoint != '.static':
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


def make_random(n=10):
    """Creates a random strings for using them as IDs."""

    return "".join(random.choice(string.ascii_lowercase + string.digits) \
            for x in range(n))


def get_dict_langs(only_codes=False):
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
        locale = l.language if only_codes else (l.language,
                                                l.display_name.capitalize())
        dicts.append(locale)

    return dicts


def require_valid_dict(f):
    """A decorator that checks whether the dictionary passed in the URL exists
    in the database or not. If not, aborts the request with 404."""

    @wraps(f)
    def decorator(dict, *args, **kwargs):
        available_dicts = get_dict_langs(only_codes=True)

        if dict not in available_dicts:
            return abort(404)

        return f(dict, *args, **kwargs)

    return decorator


def get_working_statuses(only_statuses=False):
    """Returns a list with tuples of all the available working statuses
    for a term.
    The tuple elements are status names and localized names.

    :param only_statuses: if set to True, returns a list of status names.
                          Defaults to False.
    """
    # TODO: cache items not to hit the disk each time we run this

    qs = "//adminSpec[@name='elementWorkingStatus']/contents/string()"
    statuses = dbxml.get_db().query(qs).as_str().all()

    try:
        status_split = statuses[0].split()
        # TODO: display localized names
        # TODO: limit status names depending on user privileges
        status_list = [s if only_statuses else (s, s) for s in status_split]
    except IndexError:
        status_list = []

    return status_list
