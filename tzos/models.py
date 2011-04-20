# -*- coding: utf-8 -*-
"""
    tzos.models
    ~~~~~~~~~~~

    Application models

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
import hashlib

from datetime import datetime
from time import strftime

from werkzeug import cached_property, check_password_hash, generate_password_hash

from flask import g, render_template

from flaskext.babel import gettext as _, lazy_gettext as _l
from flaskext.sqlalchemy import BaseQuery
from flaskext.principal import RoleNeed, UserNeed

from tzos.extensions import db, dbxml
from tzos.helpers import make_random

class UserQuery(BaseQuery):

    def from_identity(self, identity):
        try:
            user = self.get(int(identity.name))
        except ValueError:
            user = None

        if user:
            identity.provides.update(user.provides)

        identity.user = user

        return user

    def authenticate(self, login, password):
        user = self.filter(db.or_(User.username==login,
                                  User.email==login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated


class User(db.Model):
    __tablename__ = 'users'
    query_class = UserQuery

    # User roles
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300

    # Mapping between roles and natural names
    role_map = {
            MEMBER: _l('Member'),
            MODERATOR: _l('Moderator'),
            ADMIN: _l('Administrator'),
            }

    # Core fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    activation_key = db.Column(db.String(80), unique=True)
    role = db.Column(db.Integer, default=MEMBER)

    _password = db.Column(db.String(80))

    # Public profile fields
    display_name = db.Column(db.Unicode(80))
    website = db.Column(db.String(200))
    company = db.Column(db.Unicode(80))
    location = db.Column(db.Unicode(60))

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'),
                 UserNeed(self.id)]

        if self.is_moderator:
            needs.append(RoleNeed('moderator'))

        if self.is_admin:
            needs.append(RoleNeed('admin'))

        return needs

    @property
    def is_moderator(self):
        return self.role >= self.MODERATOR

    @property
    def is_admin(self):
        return self.role >= self.ADMIN

    @cached_property
    def natural_role(self):
        return self.role_map[self.role]

    @cached_property
    def gravatar(self):
        if not self.email:
            return ''

        md5 = hashlib.md5()
        md5.update(self.email.strip().lower())

        return md5.hexdigest()

    def gravatar_url(self, size=80):
        if not self.gravatar:
            return ''

        return "http://www.gravatar.com/avatar/%s.jpg?s=%d&d=mm" %\
            (self.gravatar, size)


class Term(object):

    def __init__(self, id=None):
        if id:
            self.term_id = id

    @property
    def id(self):
        if hasattr(self, 'term_id'):
            return self.term_id

        qs = "//term[string()='{0}']/data(@id)".format(self.term)
        result = dbxml.get_db().query(qs).as_str().first()

        if result:
            self.term_id = result

        return result

    def exists(self):
        """Returns True if the current term exists in the DB."""

        if not self.id:
            return False

        qs = "//term[@id='{0}']".format(self.id)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return True

        return False

    def has_langset(self, langcode):
        """Returns True if the current term has a langSet for langcode."""
        qs = '//langSet[@xml:lang="{0}" and ..//term[string()="{1}"]]'. \
            format(langcode, self.term)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return True

        return False

    def insert(self):
        """Inserts the current term to the DB."""

        ctx = {
            'orig_person': self.originating_person if self.not_mine else g.user.username,
            'date': strftime('%Y-%m-%d %H:%M:%S%z'),
            'username': g.user.username,
            'term_id': make_random(),
            }
        ctx.update(self.__dict__)

        if self.syntrans:
            syntrans_term = Term()
            syntrans_term.term = self.syntrans_term

            if syntrans_term.has_langset(self.language):
                template_name = 'xml/new_term.xml'
                where = '//langSet[@xml:lang="{0}"]/tig[../..//term[@id="{1}"]][1]' \
                    .format(self.language, syntrans_term.id)
            else:
                template_name = 'xml/new_langset.xml'
                where = '//langSet[..//term[@id="{0}"]][1]'.format(syntrans_term.id)
        else:
            ctx.update({'concept_id': make_random()})
            template_name = 'xml/new_concept.xml'
            where = '//termEntry[1]'

        xml = render_template(template_name, **ctx)

        if dbxml.get_db().insert_before(xml, where):
            self.term_id = ctx['term_id']
            return True

        return False
