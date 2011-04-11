# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~

    General management script

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app

from flaskext.assets import Environment, ManageAssets
from flaskext.script import Manager, prompt_bool

from tzos import create_app
from tzos import fixtures
from tzos.extensions import db, dbxml

manager = Manager(create_app)


manager.add_command("assets", ManageAssets(Environment()))

@manager.command
def createall():
    '''Creates the SQL tables needed by the models.'''

    db.create_all()

@manager.command
def dropall():
    '''Deletes all the SQL database data.'''

    if prompt_bool('Are you sure? This will delete all the data.'):
        db.drop_all()

@manager.command
def initdb():
    '''Initializes some basic data to start playing with the app.'''
    # TODO: find a way to check if the db schema has been initialized

    fixtures.install()

@manager.option('-f', '--filename', dest='filename', default=None, required=True)
@manager.option('-d', '--docname', dest='docname', default=None)
def initdbxml(filename, docname):
    '''Initializes the XML-DB by feeding data from the given file.'''

    dbxml.init_dbxml(filename, docname)

@manager.shell
def make_shell_context():
    return dict(app=current_app)

manager.add_option('-c', '--config',
                   default='config.py',
                   dest='config',
                   required=False)

if __name__ == "__main__":
    manager.run()
