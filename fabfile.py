#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Fabric deployment file.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from fabric.api import cd, env
from fabric.context_managers import hide, prefix, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, upload_template
from fabric.operations import put, run, sudo

from configs import fabric


#
# Load server settings from the configuration module
#

env.hosts = fabric.HOSTS
env.user = fabric.USER

env.project_name = fabric.PROJECT_NAME
env.project_path = fabric.PROJECT_PATH
env.project_repo = fabric.PROJECT_REPO
env.project_url = fabric.PROJECT_URL
env.project_settings = fabric.PROJECT_SETTINGS

env.vhost_dir = fabric.VHOST_DIR
env.vhost_file = fabric.VHOST_FILE

env.wsgi_file = fabric.WSGI_FILE
env.wsgi_user = fabric.WSGI_USER
env.wsgi_group = fabric.WSGI_GROUP


def bootstrap():
    """Creates initial directories and virtual environment."""

    if (exists('%(project_path)s' % env) and \
        confirm('%(project_path)s already exists. Do you want to continue?' \
                % env, default=False)) or not exists('%(project_path)s' % env):

            print('Bootstrapping initial directories...')

            with settings(hide('warnings', 'running', 'stdout', 'stderr')):

                sudo('mkdir -p %(project_path)s' % env)
                sudo('chown %(user)s:%(user)s %(project_path)s' % env)

                with cd(env.project_path):

                    run('git clone %(project_repo)s .' % env)
                    run('virtualenv --no-site-packages env')

                    with settings(warn_only=True):
                        run('mkdir -m a+w logs')
                        run('mkdir -m g+w tzos/dbs')

    else:

        print('Aborting.')


def deploy():
    """Updates the code and installs the production site."""

    print('Deploying the site...')

    update_code()
    install_site()


def update_code():
    """Updates the code used in the production environment."""

    print('Getting the latest code and dependencies...')

    with settings(hide('warnings', 'running', 'stdout', 'stderr')):

        with cd(env.project_path):

            run('git pull')
            run('pip install -E env/ -r requirements.txt')


def install_site():
    """Updates the configuration and enables the site."""

    print('Configuring and installing site...')

    update_config()
    enable_site()


def update_config():
    """Updates configuration files (Apache, WSGI, app)."""

    with settings(hide('warnings', 'running', 'stdout', 'stderr')):

        # Configure VirtualHost
        upload_template('configs/virtualhost.conf', '%(vhost_file)s' % env,
                        context=env, use_jinja=True, use_sudo=True)

        # Configure WSGI application
        upload_template('configs/tzos.wsgi', '%(wsgi_file)s' % env,
                        context=env, use_jinja=True)

        # Configure and install production settings
        upload_template('configs/production.py', '%(project_settings)s' % env,
                        context=env, use_jinja=True)


def enable_site():
    """Enables the site."""

    _switch_site(True)


def disable_site():
    """Disables the site."""

    _switch_site(False)


def _switch_site(enable):
    """Switches site's status to enabled or disabled."""

    action = "Enabling" if enable else "Disabling"
    print('%s site...' % action)

    with settings(hide('warnings', 'running', 'stdout', 'stderr')):

        env.apache_command = 'a2ensite' if enable else 'a2dissite'

        sudo('%(apache_command)s %(project_name)s' % env)

        with settings(warn_only=True):
            sudo('/etc/init.d/apache2 reload')


def touch():
    """Runs 'touch' on the WSGI file to reload daemon processes."""

    print('Running touch...')

    run('touch %(wsgi_file)s' % env)


def copy_local_dbs():
    """Copies local db data to play with the application."""

    print('Copying local dbs to the server...')

    with settings(warn_only=True):

        put('tzos/dbs/*', env.project_path + '/tzos/dbs/', mode=0664)
        put('tzos/dbs/dbxml/*', env.project_path + '/tzos/dbs/dbxml/', mode=0664)


def compile_translations():
    """Compiles PO translations."""

    print('Compiling translations...')

    with cd(env.project_path):

        with prefix('source env/bin/activate' % env):

            run('pybabel compile -d tzos/translations')

