# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~

    Helper functions

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import _request_ctx_stack, abort, current_app, g, request, url_for

from babel import Locale
from functools import wraps

from tzos.extensions import dbxml
from tzos import strings

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


def get_all_langs(only_codes=False):
    """Returns a list with tuples of all the languages known by Babel.
    The tuple elements are language codes and language names.

    :param only_codes: if set to True, returns a list of language codes.
                       Defaults to False.
    """
    langs = []

    from babel import localedata

    for code in localedata.list():
        l = Locale.parse(code)
        locale = l.language if only_codes else (l.language,
                                                l.display_name)
        langs.append(locale)

    return langs


def get_dict_langs(only_codes=False):
    """Returns a list with tuples of all the available dictionaries.
    The tuple elements are language codes and language names.

    :param only_codes: if set to True, returns a list of language codes.
                       Defaults to False.
    """
    # TODO: cache items not to hit the disk each time we run this
    dicts = []

    qs = "//languages/langInfo/langCode/string()"
    dictlist = dbxml.get_db().query(qs).as_str().all()

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


def get_responsible_orgs():
    """Returns a list with tuples of all the available responsible
    organizations. These organizations are to be used in
    normativeAuthorization fields.

    The tuple elements are organization IDs and display names.
    """
    # TODO: cache items not to hit the disk each time we run this

    qs = """
    for $org in collection("{0}")//refObjectList[@type='respOrg']/refObject
    return ($org/data(@id), $org/item[@type='org']/string())
    """.format(dbxml.get_db().collection)
    result = dbxml.get_db().raw_query(qs).as_str().all()

    orgs_list = zip(result, result[1:])[::2]

    return orgs_list


def dropdown_list(list):
    """Inserts a placeholder tuple entry in a list, suitable for using
    in dropdown lists."""

    newlist = list[:]
    newlist.insert(0, ('none', '-----'))

    return newlist
