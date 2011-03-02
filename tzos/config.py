
DEBUG = True

SECRET_KEY = 'f00barbaZ'

# TZOS stuff
TZOS_DEFAULT_DICT = 'eu'

# SQLAlchemy database settings
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/julen/dev/tzos/tzos/dbs/tzos.db'
SQLALCHEMY_ECHO = False

# DB-XML database settings
DBXML_DATABASE = '/home/julen/dev/tzos/tzos/dbs/tzos.dbxml'

# Babel configuration settings
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'CET'

# Mail settings
#MAIL_SERVER = 'localhost'
#MAIL_PORT = 25
#MAIL_USE_TLS = False
#MAIL_USE_SSL = False
#MAIL_USERNAME = foo
#MAIL_PASSWORD = bar
DEFAULT_MAIL_SENDER = ('TZOS', 'no-reply@tzos.net')
MAIL_FAIL_SILENTLY = DEBUG

# Recaptcha settings
RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = '6LchVcASAAAAAGfvqAQAQEkq2K-YIOeG9HlAtVln'
RECAPTCHA_PRIVATE_KEY = '6LchVcASAAAAAHU6lMuS8BaBoC5goiMwbGry1KHs'

# Assets settings
ASSETS_DEBUG = DEBUG
