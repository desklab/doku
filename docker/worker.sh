#!/bin/bash
export DOKU_CONFIG=config.prod
celery --app tasks.celery worker
