export DOKU_CONFIG=config.prod
alembic upgrade head
uwsgi --ini /app/etc/uwsgi.ini