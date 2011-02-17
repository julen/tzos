# -*- coding: utf-8 -*-
"""
    tzos.extensions
    ~~~~~~~~~~~~~~~

    Extensions available through the app

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.mail import Mail
from flaskext.dbxml import DBXML
from flaskext.sqlalchemy import SQLAlchemy

__all__ = ['db', 'dbxml', 'mail']

db = SQLAlchemy()
dbxml = DBXML()
mail = Mail()
