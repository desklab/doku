from flask import Flask

from doku.blueprints.api import v1
from doku.blueprints.api.v1 import document, template, variable, stylesheet


def init_api(app: Flask):
    app.register_blueprint(v1.bp, url_prefix="/api/v1")
    app.register_blueprint(document.bp, url_prefix="/api/v1/document")
    app.register_blueprint(template.bp, url_prefix="/api/v1/template")
    app.register_blueprint(variable.bp, url_prefix="/api/v1/variable")
    app.register_blueprint(stylesheet.bp, url_prefix="/api/v1/stylesheet")
