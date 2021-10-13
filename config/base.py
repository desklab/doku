import os
import socket
from logging.config import dictConfig

from .util import get_env_read_file

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = b"dont_use_this_in_production"

TEMPLATE_FOLDER = "templates"
STATIC_FOLDER = os.path.join("static", "dist")

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Add the current host
ALLOWED_HOSTS.append(socket.gethostname())

if get_env_read_file("DOKU_HOST", None) is not None:
    ALLOWED_HOSTS.append(os.environ["DOKU_HOST"])

dictConfig(
    {
        "version": 1,
        "formatters": {"default": {"format": "%(message)s",}},
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

REDIS_CONFIG = {
    "host": get_env_read_file("REDIS_HOST", "localhost"),
    "port": get_env_read_file("REDIS_PORT", 6379),
    "password": get_env_read_file("REDIS_PASSWORD", None),
}

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Local Storage
UPLOAD_FOLDER = os.path.join(BASE_DIR, "resources")
SHARED_FOLDER = os.path.join(BASE_DIR, "shared")  # used for tasks

# CSRF Settings
CSRF_COOKIE_NAME = "csrf_token"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_HEADER_NAME = "X-CSRF-TOKEN"

# Session Settings
SESSION_PREFIX = "doku_session_"
SESSION_COOKIE_NAME = "doku_session"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Sentry Settings
SENTRY_DSN = get_env_read_file("SENTRY_DSN", None)

# Celery Settings
CELERY_BROKER_URL = f"redis://{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}/0"
CELERY_CONFIG = {
    "result_backend": CELERY_BROKER_URL,
    "broker_url": CELERY_BROKER_URL,
    "worker_redirect_stdouts_level": "INFO"
}

# Download Requests
PENDING_DOWNLOAD_LIMIT = 5

# API
API_TOKEN_LENGTH = 32
API_TOKEN_STORAGE_PREFIX = "doku_api_token_"
API_TOKEN_STORAGE_EXPIRATION = 3600
API_TOKEN_SALT = "salty_token"

try:
    from .local import *
except ImportError:
    pass
