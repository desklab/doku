import os
from importlib import import_module

import click
from flask_babel import Babel
from sqlalchemy.sql import exists
from flask import Flask, request
from flask.cli import FlaskGroup
from redis import Redis
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from doku.models import db
from doku.models import base
from doku.blueprints import auth, base, document, template, resources
from doku.blueprints import api
from doku.utils.middlewares.csrf import CSRFMiddleware, csrf
from doku.utils.middlewares.hosts import host_middleware
from doku.utils.session import RedisSessionInterface


def create_app(name="doku",
        config=None,
        minimal=False,
        test=False,
        additional_config=None
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
    config = os.environ.get("DOKU_CONFIG", "config.dev")
    if test:
        # Overwrite the config parameter to use a testing environment
        config = "config.test"
    config_module = import_module(config)

    # Only initialize sentry if in production and SENTRY_DSN is set
    _env = os.environ.get("FLASK_ENV", "development")
    if _env == "production" and config_module.SENTRY_DSN is not None:
        sentry_sdk.init(dsn=config_module.SENTRY_DSN, integrations=[FlaskIntegration()])

    app = Flask(name, instance_relative_config=True)
    app.config.from_object(config_module)
    app.static_url_path = app.config.get("STATIC_FOLDER")
    app.static_folder = os.path.join(app.root_path, app.static_url_path)

    if additional_config is not None:
        app.config.update(additional_config)

    redis = Redis(**app.config["REDIS_CONFIG"])
    app.session_interface = RedisSessionInterface(
        app, redis, app.config.get("SESSION_PREFIX", "session_")
    )

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    # Flask extensions
    babel = Babel(app)
    db.init_app(app)

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
        app.register_blueprint(document.bp, url_prefix="/document")
        app.register_blueprint(template.bp, url_prefix="/template")
        app.register_blueprint(resources.bp, url_prefix="/resources")
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
