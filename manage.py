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
from flaskext.script import Manager, prompt_bool, Server

from tzos import create_app
from tzos import fixtures
from tzos.extensions import db, dbxml

manager = Manager(create_app)


manager.add_command("assets", ManageAssets(Environment()))


class CustomServer(Server):

    def __init__(self, *args, **kwargs):

        server_opts = {'threaded': True}
        super(CustomServer, self).__init__(*args, **server_opts)

manager.add_command('runserver', CustomServer())


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
def add_document(filename, docname):
    '''Adds a document to the XML-DB by feeding data from the given file.'''

    dbxml.add_document(filename, docname)

@manager.option('-d', '--docname', dest='docname', default=None)
def rm_document(docname):
    '''Removes a document from the XML-DB that matches the given name.'''

    dbxml.rm_document(docname)

@manager.command
def add_indexes():
    '''Adds proper indexes to the DB-XML container.'''

    indexes = [
        ('', 'id', 'node-attribute-equality-string edge-attribute-equality-string'),
        ('', 'term',
            'node-element-equality-string node-element-substring-string'),
        ('', 'type', 'node-attribute-equality-string edge-attribute-equality-string'),
        ('http://www.w3.org/1999/xhtml',
            'lang', 'node-attribute-equality-string'),
        ('', 'admin', 'node-element-equality-string'),
        ('', 'descrip', 'node-element-equality-string'),
        ('', 'ref', 'node-element-equality-string'),
        ('', 'termNote', 'node-element-equality-string'),
    ]

    dbxml.add_indexes(indexes)

@manager.shell
def make_shell_context():
    return dict(app=current_app)

manager.add_option('-c', '--config',
                   default='config.py',
                   dest='config',
                   required=False)

if __name__ == "__main__":
    manager.run()
