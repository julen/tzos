# -*- coding: utf-8 -*-
"""
    tzos.fixtures
    ~~~~~~~~~~~~~

    Default application data

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from tzos.extensions import db
from tzos.models import User

def install():
    """Installs the initial fixtures in the database."""

    create_initial_users()

def create_initial_users():
    admin = User()
    admin.username = u'admin'
    admin.password = u'admin'
    admin.email = u'admin@tzos.net'
    admin.role = User.ADMIN
    admin.display_name = u'Default Administrator'

    supervisor = User()
    supervisor.username = u'supervisor'
    supervisor.password = u'supervisor'
    supervisor.email = u'supervisor@tzos.net'
    supervisor.role = User.MODERATOR
    supervisor.display_name = u'Default supervisor'

    member = User()
    member.username = u'member'
    member.password = u'member'
    member.email = u'member@tzos.net'
    member.role = User.MEMBER
    member.display_name = u'Default member'

    db.session.add(admin)
    db.session.add(supervisor)
    db.session.add(member)
    db.session.commit()
