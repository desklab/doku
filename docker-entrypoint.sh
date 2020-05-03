export DOKU_CONFIG=config.prod
gunicorn wsgi:app --name doku --bind 0.0.0.0:8000 --workers 5
