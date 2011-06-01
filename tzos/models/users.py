# -*- coding: utf-8 -*-
"""
    tzos.models.users
    ~~~~~~~~~~~~~~~~~

    User models.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
import hashlib

from datetime import datetime

from werkzeug import cached_property, check_password_hash, generate_password_hash

from flaskext.babel import gettext as _, lazy_gettext as _l
from flaskext.sqlalchemy import BaseQuery
from flaskext.principal import RoleNeed, UserNeed

from tzos.extensions import db, dbxml

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

    def owns_term(self, id):
        """Returns True if the current user owns the term with id `id`."""

        qs = '//tig[@id="{0}" and transacGrp/transacNote[@type="responsibility"]/string()="{1}"]'.format(id, self.username)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return True

        return False
