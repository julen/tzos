# -*- coding: utf-8 -*-
"""
    tzos.pagination
    ~~~~~~~~~~~~~~~

    Random object pagination.

    Code mostly taken from Flask-SQLAlchemy.
    https://github.com/mitsuhiko/flask-sqlalchemy/

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from math import ceil

from flask import abort


def paginate(obj, page, per_page, error_out=True):

    if error_out and page < 1:
        abort(404)

    offset = (page - 1) * per_page
    last = offset + per_page

    items = obj[offset:last]

    if not items and page != 1 and error_out:
        abort(404)

    return Pagination(page, per_page, len(obj), items)


class Pagination(object):

    def __init__(self, page, per_page, total, items):

        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        return int(ceil(self.total / float(self.per_page)))

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
