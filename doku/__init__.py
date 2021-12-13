__version__ = "0.3.2"
__author__ = "Jonas Drotleff <j.drotleff@desk-lab.de>"
__all__ = ["create_app", "cli"]


import os
from importlib import import_module
from typing import Optional

import click
from flask_babel import Babel
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.sql import exists
from flask import Flask, request
from flask.cli import FlaskGroup
from redis import Redis
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from doku.models import db
from doku.tasks import celery
from doku.models import base

from doku.blueprints import (
    auth,
    base,
    document,
    template,
    resources,
    account,
    snippet,
    stylesheets,
)
from doku.blueprints import api
from doku.utils.middlewares.csrf import CSRFMiddleware, csrf
from doku.utils.middlewares.hosts import host_middleware
from doku.utils.session import RedisSessionInterface


def create_app(
    name="doku",
    config: str = "config.dev",
    minimal: bool = False,
    test: bool = False,
    additional_config: Optional[dict] = None,
) -> Flask:
    """
    App Factory - create_app

    This is the doku Flask app factory

    :param name: Name of the application. Defaults to ``doku``
    :param config: Pythonic path (``path.to.module``) for the
        configuration file
    :param minimal: Set this to ``True`` for a minimal version
        of the flask app. This will disable middlewares, blueprints and
        other non-essential extensions but return a usable app which
        can be used for database operations (e.g. in the context of
        tasks).
        Note that this will not yield a functional webapp. Most routes
        may not be initialized. Only the key functions are served.
    :param test: Enable the testing environment. This will overwrite
        the ``config`` parameter.
    """
    config = os.environ.get("DOKU_CONFIG", config)
    if test:
        # Overwrite the config parameter to use a testing environment
        config = "config.test"
    # Import the configuration object
    config_module = import_module(config)
    # Only initialize sentry if in production and SENTRY_DSN is set
    _env = os.environ.get("FLASK_ENV", "development")
    _sentry_dsn = getattr(config_module, "SENTRY_DSN", None)
    if _env == "production" and _sentry_dsn is not None:
        sentry_sdk.init(
            dsn=_sentry_dsn,
            release=f"doku@{__version__}",
            integrations=[
                FlaskIntegration(),
                RedisIntegration(),
                SqlalchemyIntegration(),
            ],
        )

    app = Flask(name)
    app.config.from_object(config_module)
    app.static_url_path = app.config.get("STATIC_FOLDER")
    app.static_folder = os.path.join(app.root_path, app.static_url_path)
    # Additional config might be needed for tests
    if additional_config is not None:
        app.config.update(additional_config)
    # Prepare redis for session and tasks
    redis = Redis(**app.config["REDIS_CONFIG"])
    app.session_interface = RedisSessionInterface(
        app, redis, app.config.get("SESSION_PREFIX", "session_")
    )
    app.redis = redis
    # Prepare celery for tasks
    if not hasattr(config_module, "CELERY_CONFIG"):
        raise ValueError("'CELERY_CONFIG' not provided in configuration")
    celery.conf.update(**getattr(config_module, "CELERY_CONFIG"))

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(app.config["SHARED_FOLDER"]):
        os.makedirs(app.config["SHARED_FOLDER"])
    # Flask extensions
    babel = Babel(app)
    db.init_app(app)

    if not minimal:

        @babel.localeselector
        def get_locale():
            return request.accept_languages.best_match(["de", "en"])

    # WSGI middlewares
    if not minimal:
        csrf.init_app(app)
        host_middleware(app)

    # Blueprints
    if not minimal:
        app.register_blueprint(base.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(account.bp, url_prefix="/account")
        app.register_blueprint(document.bp, url_prefix="/document")
        app.register_blueprint(template.bp, url_prefix="/template")
        app.register_blueprint(resources.bp, url_prefix="/resources")
        app.register_blueprint(stylesheets.bp, url_prefix="/stylesheets")
        app.register_blueprint(snippet.bp, url_prefix="/snippet")
        api.init_api(app)

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """
    doku Command Line Interface

    Uses the default ``FlaskGroup`` to provide the default flask
    interface with commands such as ``run``, ``shell``, etc.
    """
    pass


@cli.command("create-user", help="Create new user")
def create_user():
    import getpass
    from doku.models.user import User

    app = cli.create_app(minimal=True)
    default_username = getpass.getuser()

    with app.app_context():
        username = None
        while not username:
            username = click.prompt("User name", default=default_username)
            if db.session.query(exists().where(User.username == username)).scalar():
                click.secho(
                    f"User with username {username} already exists!", fg="red", err=True
                )
                username = None

        email = None
        while not email:
            email = input("E-Mail: ") or None
            if not email:
                click.secho("This field can not be left empty!", fg="red", err=True)

        password = None
        while not password:
            password = getpass.getpass(f"Password: ")
            if not password:
                click.secho("This field can not be left empty!", fg="red", err=True)

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        click.secho(f"Created user {user.username}", fg="green")


@cli.command("init-db")
def init_db():
    app: Flask = cli.create_app(minimal=True)
    with app.app_context():
        db.create_all(app=app)
        click.secho(f"Initialized database", fg="green")
