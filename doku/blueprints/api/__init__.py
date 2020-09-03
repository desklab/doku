from werkzeug.exceptions import BadRequest, Unauthorized
from marshmallow.exceptions import ValidationError
from flask import Flask, request, session, Blueprint, jsonify

from doku.blueprints.api import v1
from doku.blueprints.api.v1 import document, template, variable, stylesheet, resource, \
    snippet
from doku.models.user import User


def api_auth():
    token = request.headers.get("Authorization", None)
    if token is not None and "Bearer" in token:
        auth = User.token_auth(token)
        if auth is None:
            raise Unauthorized()
        else:
            session.update(auth)
            session.authenticated = True
            session.nosave = True


def auth_required():
    if not hasattr(session, "authenticated") or not session.authenticated:
        raise Unauthorized("You need to login first")


def handle_api_error(error):
    if hasattr(error, "code"):
        error_code = error.code
    else:
        error_code = BadRequest.code
    response = jsonify({"success": False, "error": error.description})
    response.status_code = error_code
    return response


def handle_validation_error(error: ValidationError):
    if not isinstance(error, ValidationError):
        raise ValueError("Can only handle ValidationError")
    response = jsonify({"success": False, "error": error.normalized_messages()})
    response.status_code = BadRequest.code
    return response


def register(app: Flask, blueprint: Blueprint, auth=False, **kwargs):
    blueprint.register_error_handler(BadRequest, handle_api_error)
    blueprint.register_error_handler(Unauthorized, handle_api_error)
    blueprint.register_error_handler(ValidationError, handle_validation_error)
    blueprint.before_request(api_auth)
    if auth:
        blueprint.before_request(auth_required)
    app.register_blueprint(blueprint, **kwargs)


def init_api(app: Flask):
    register(app, v1.bp, auth=False, url_prefix="/api/v1")
    register(app, document.bp, auth=True, url_prefix="/api/v1/document")
    register(app, template.bp, auth=True, url_prefix="/api/v1/template")
    register(app, variable.bp, auth=True, url_prefix="/api/v1/variable")
    register(app, stylesheet.bp, auth=True, url_prefix="/api/v1/stylesheet")
    register(app, resource.bp, auth=True, url_prefix="/api/v1/resource")
    register(app, snippet.bp, auth=True, url_prefix="/api/v1/snippet")
