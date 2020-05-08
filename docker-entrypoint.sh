export DOKU_CONFIG=config.prod
alembic upgrade head
gunicorn wsgi:app --name doku --bind 0.0.0.0:8000 --workers 3
