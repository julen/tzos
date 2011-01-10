
DEBUG = True

SECRET_KEY = 'f00barbaZ'

# SQLAlchemy database settings
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/julen/dev/tzos/tzos.db'
SQLALCHEMY_ECHO = DEBUG

# Babel configuration settings
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC+1'

# Recaptcha settings
RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = '6LchVcASAAAAAGfvqAQAQEkq2K-YIOeG9HlAtVln'
RECAPTCHA_PRIVATE_KEY = '6LchVcASAAAAAHU6lMuS8BaBoC5goiMwbGry1KHs'
