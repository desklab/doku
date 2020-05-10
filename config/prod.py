import os
from .base import *

SECRET_KEY = os.environ.get('DOKU_SECRET')
DEBUG = False
TESTING = False
FLASK_ENV = 'production'

PREFERRED_URL_SCHEME = 'https'
SERVER_NAME = 'doku.desk-lab.de'

sql_password = os.environ.get('DOKU_DB_PASSWORD')
sql_user = os.environ.get('DOKU_DB_USER')
sql_host = os.environ.get('DOKU_DB_HOST')
sql_db = os.environ.get('DOKU_DB_DATABASE')
SQLALCHEMY_DATABASE_URI = \
    f'postgresql://{sql_user}:{sql_password}@{sql_host}/{sql_db}'


# CSRF Settings
CSRF_COOKIE_SECURE = True

# Session Settings
SESSION_COOKIE_SECURE = True
