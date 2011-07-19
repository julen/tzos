# -*- coding: utf-8 -*-
"""
    tzos.models.comments
    ~~~~~~~~~~~~~~~~~~~~

    Comment models.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from werkzeug import cached_property

from tzos.extensions import db
from tzos.models.types import DenormalizedText
from tzos.models.terms import Term
from tzos.models.users import User

class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)

    term_id = db.Column(db.Integer, nullable=False)

    comment = db.Column(db.UnicodeText)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.Column(DenormalizedText)

    author = db.relation(User, innerjoin=True, lazy="joined")


    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        self.votes = self.votes or set()

    def vote(self, user):
        self.votes.add(user.id)

    @cached_property
    def term(self):
        return Term(self.term_id)

    def _url(self, _external=False):
        return '%s#comment-%d' % (self.term._url(_external), self.id)

    @cached_property
    def url(self):
        return self._url()

    @cached_property
    def permalink(self):
        return self._url(True)

