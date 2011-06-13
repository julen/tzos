# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~

    Helper functions

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import Markup, _request_ctx_stack, abort, current_app, g, \
        request, url_for

from babel import Locale
from functools import wraps

from tzos.extensions import cache, dbxml
from tzos.models import Term, TermOrigin
from tzos import strings

import functools
import random
import string
import types


def url_for2(endpoint, **values):
    """Overriden method to always add request.view_args."""

    if endpoint != '.static':
        values.update(request.view_args)

        # Non-destructive merge for request.args
        for k, v in request.args.iteritems():
            values.setdefault(k, v)

    return url_for(endpoint, **values)


def tzos_gettext(key):
    """Special method to retrieve strings stored in the strings module."""
    contexts = [k for k in dir(strings) \
            if type(getattr(strings, k)) == types.ListType]

    for ctx in contexts:
        str_list = getattr(strings, ctx)

        for elem in str_list:
            if str(elem[0]) == key:
                return elem[1]

    return key

anon_cached = functools.partial(cache.cached,
                                unless=lambda: g.user is not None)

@cache.memoize()
def get_dict_langs(only_codes=False):
    """Returns a list with tuples of all the available dictionaries.
    The tuple elements are language codes and language names.

    :param only_codes: if set to True, returns a list of language codes.
                       Defaults to False.
    """
    dicts = []

    qs = u"/TBXXCS/languages/langInfo/langCode/string()"
    dictlist = dbxml.session.query(qs, document='tzos.xcs').as_str().all()

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


@cache.memoize()
def get_working_statuses(only_statuses=False):
    """Returns a list with tuples of all the available working statuses
    for a term.
    The tuple elements are status names and localized names.

    :param only_statuses: if set to True, returns a list of status names.
                          Defaults to False.
    """

    qs = u"//adminSpec[@name='elementWorkingStatus']/contents/string()"
    statuses = dbxml.session.query(qs).as_str().all()

    try:
        status_split = statuses[0].split()
        # TODO: display localized names
        # TODO: limit status names depending on user privileges
        status_list = [s if only_statuses else (s, s) for s in status_split]
    except IndexError:
        status_list = []

    return status_list


@cache.memoize()
def get_responsible_orgs():
    """Returns a list with tuples of all the available responsible
    organizations. These organizations are to be used in
    normativeAuthorization fields.

    The tuple elements are organization IDs and display names.
    """

    qs = """
    for $org in collection("{0}")//refObjectList[@type='respOrg']/refObject
    return ($org/data(@id), $org/item[@type='org']/string())
    """.format(dbxml.session.collection)
    result = dbxml.session.raw_query(qs).as_str().all()

    orgs_list = zip(result, result[1:])[::2]

    return orgs_list


def get_origins_dropdown():
    """Returns a list of (key, value) tuples including all the allowed
    conceptOrigins."""

    def _get_children(parent_id, depth):

        for origin in origins:

            if origin.parent_id == parent_id:
                name = Markup((u'&nbsp;' * 3) * depth + origin.name).unescape()
                dropdown.append((origin.id, name))

                if origin.children:
                    _get_children(origin.id, depth + 1)

    dropdown = []
    origins = TermOrigin.query.order_by('name').all()
    parents = [(o.id, o.name) for o in origins if o.parent_id is None]

    for id, name in parents:
        dropdown.append((id, name))
        _get_children(id, 1)

    return dropdown
