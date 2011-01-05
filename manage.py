# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~

    General management script

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app

from flaskext.script import Manager

from tzos import create_app

manager = Manager(create_app)

@manager.shell
def make_shell_context():
    return dict(app=current_app)

manager.add_option('-c', '--config',
                   default='config.py',
                   dest='config',
                   required=False)

if __name__ == "__main__":
    manager.run()
