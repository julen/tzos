# -*- coding: utf-8 -*-
"""
    tzos.models.translations
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Translation models.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from tzos.extensions import db

class Translation(db.Model):
    __tablename__ = 'translations'
    __table_args__ = (db.UniqueConstraint('id', 'locale'), {})

    auto_id = db.Column(db.Integer, primary_key=True)

    id = db.Column(db.Integer)

    locale = db.Column(db.String(2), default='en', nullable=False)

    text = db.Column(db.UnicodeText)

    __mapper_args__ = {'order_by' : text.asc()}
