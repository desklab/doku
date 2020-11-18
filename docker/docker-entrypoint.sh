export DOKU_CONFIG=config.prod
alembic upgrade head
uwsgi --ini uwsgi.ini