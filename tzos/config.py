
DEBUG = True

SECRET_KEY = 'f00barbaZ'

# TZOS stuff
TZOS_DEFAULT_DICT_LANG = 'eu'

# Caching
CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300

# SQLAlchemy database settings
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/julen/dev/tzos/tzos/dbs/tzos.db'
SQLALCHEMY_ECHO = False

# DB-XML database settings
DBXML_ENV = '/home/julen/dev/tzos/tzos/dbs/dbxml/'
DBXML_DATABASE = DBXML_ENV + 'tzos.dbxml'
DBXML_BASE_URI = 'file:///home/julen/dev/tzos/tzos/templates/xquery/'
DBXML_CACHESIZE_GB = 0
DBXML_CACHESIZE_BYTES = 512 * 1024 * 1024

# Babel configuration settings
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'CET'

# Mail settings
#MAIL_SERVER = 'localhost'
#MAIL_PORT = 25
#MAIL_USE_TLS = False
#MAIL_USE_SSL = False
#MAIL_USERNAME = 'foo'
#MAIL_PASSWORD = 'bar'
DEFAULT_MAIL_SENDER = ('TZOS', 'no-reply@tzos.net')
MAIL_FAIL_SILENTLY = not DEBUG

# Recaptcha settings
RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = '6LchVcASAAAAAGfvqAQAQEkq2K-YIOeG9HlAtVln'
RECAPTCHA_PRIVATE_KEY = '6LchVcASAAAAAHU6lMuS8BaBoC5goiMwbGry1KHs'

# Assets settings
ASSETS_DEBUG = DEBUG
