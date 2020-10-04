import os
from importlib import import_modules

from doku.tasks import celery
from doku.tasks.base import *

config = os.environ.get("DOKU_CONFIG", "config.dev")
config_module = import_module(config)

celery.conf.update(**config_module.CELERY_CONFIG)
