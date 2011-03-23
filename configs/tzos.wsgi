#!/usr/bin/env python

import os
import site
import sys

site.addsitedir('{{ project_path }}/env/lib/python2.6/site-packages/')

sys.path.append('{{ project_path }}')

os.environ['TZOS_CONFIG'] = '{{ project_path }}/tzos/production.py'

from tzos import create_app
application = create_app()
