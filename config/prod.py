import os
from .base import *

SECRET_KEY = get_env_read_file("DOKU_SECRET")
DEBUG = False
TESTING = False
FLASK_ENV = "production"

PREFERRED_URL_SCHEME = "https"
SERVER_NAME = None

# Adjust for server name
# ALLOWED_HOSTS = ['example.org']

sql_password = get_env_read_file("DOKU_DB_PASSWORD")
sql_user = get_env_read_file("DOKU_DB_USER")
sql_host = get_env_read_file("DOKU_DB_HOST")
sql_db = get_env_read_file("DOKU_DB_DATABASE")
SQLALCHEMY_DATABASE_URI = f"postgresql://{sql_user}:{sql_password}@{sql_host}/{sql_db}"


# CSRF Settings
CSRF_COOKIE_SECURE = True

# Session Settings
SESSION_COOKIE_SECURE = True

UPLOAD_FOLDER = os.environ.get("DOKU_UPLOAD_FOLDER", "/app/resources")
SHARED_FOLDER = os.environ.get("DOKU_UPLOAD_FOLDER", "/app/shared")
