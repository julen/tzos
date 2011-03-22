#!/usr/bin/env python

import os
import site
import sys

site.addsitedir('PROJECT_PATH/env/lib/python2.6/site-packages/')
site.addsitedir('PROJECT_PATH/flask-dbxml/')

sys.path.append(PROJECT_PATH)

os.environ['TZOS_CONFIG'] = 'PROJECT_PATH/tzos/prod_config.py'

from tzos import create_app
application = create_app()
