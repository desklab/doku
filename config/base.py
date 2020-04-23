import os
from logging.config import dictConfig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = b'dont_use_this_in_production'

TEMPLATE_FOLDER = 'templates'
STATIC_FOLDER = os.path.join('static', 'dist')

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

SESSION_PREFIX = 'doku_session_'
SQLALCHEMY_TRACK_MODIFICATIONS = False
