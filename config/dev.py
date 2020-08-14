from .base import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FLASK_ENV = "development"
ENV = FLASK_ENV
DEBUG = True
TESTING = False
os.environ.setdefault("FLASK_DEBUG", "1")
os.environ.setdefault("FLASK_ENV", FLASK_ENV)

_DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{_DATABASE_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
