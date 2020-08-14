#!/bin/bash
export DOKU_CONFIG=config.prod
celery worker -A tasks.celery --loglevel=info
