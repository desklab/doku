from .base import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FLASK_ENV = "development"
ENV = FLASK_ENV
DEBUG = True
TESTING = False
os.environ.setdefault("FLASK_DEBUG", "1")
os.environ.setdefault("FLASK_ENV", FLASK_ENV)

_DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
# SQLALCHEMY_DATABASE_URI = f"sqlite:///{_DATABASE_PATH}"
# SQLALCHEMY_TRACK_MODIFICATIONS = False


###########
# Postgres
###########
sql_password = os.environ.get("DOKU_DB_PASSWORD", "password_doku")
sql_user = os.environ.get("DOKU_DB_USER", "doku_user")
sql_host = os.environ.get("DOKU_DB_HOST", "localhost")
sql_db = os.environ.get("DOKU_DB_DATABASE", "doku_db")
SQLALCHEMY_DATABASE_URI = f"postgresql://{sql_user}:{sql_password}@{sql_host}/{sql_db}"
