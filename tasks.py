import os

from doku.tasks import celery
from doku.tasks.base import *

config = os.environ.get("DOKU_CONFIG", "config.dev")
celery.config_from_object(config)
