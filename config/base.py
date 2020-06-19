import os
from logging.config import dictConfig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = b'dont_use_this_in_production'

TEMPLATE_FOLDER = 'templates'
STATIC_FOLDER = os.path.join('static', 'dist')

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1"
]

if os.environ.get("DOKU_HOST", None) is not None:
    ALLOWED_HOSTS.append(os.environ["DOKU_HOST"])

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

REDIS_CONFIG = {
    'host': os.environ.get('REDIS_HOST', 'localhost'),
    'port': os.environ.get('REDIS_PORT', 6379),
    'password': os.environ.get('REDIS_PASSWORD', None)
}

SQLALCHEMY_TRACK_MODIFICATIONS = False

# File upload
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'resources')

# CSRF Settings
CSRF_COOKIE_NAME = 'csrf_token'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_HEADER_NAME = 'X-CSRF-TOKEN'

# Session Settings
SESSION_PREFIX = 'doku_session_'
SESSION_COOKIE_NAME = 'doku_session'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Sentry Settings
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)

try:
    from .local import *
except ImportError:
    pass
