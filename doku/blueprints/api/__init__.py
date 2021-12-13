from typing import Union

from werkzeug.exceptions import BadRequest, Unauthorized
from marshmallow.exceptions import ValidationError
from flask import Flask, request, session, Blueprint, jsonify

from doku.blueprints.api import v1
from doku.blueprints.api.v1 import (
    document,
    template,
    variable,
    stylesheet,
    resource,
    snippet,
    vargroup,
)
from doku.models.user import User


def api_auth():
    """Authentication Procedure for API

    This function is used as a middleware for authenticating an API user
    using the session interface. Using
    :meth:`Flask.flask.Blueprint.before_request`, this function will be
    called before each request to an API endpoint. When credentials are
    provided through the ``Authorization`` header, the token is used
    for authentication using the :meth:`doku.model.User.token_auth`
    class method.

    For more information about constructing a valid authentication
    token, see :meth:`doku.model.User.token_auth`.

    :raises: :class:`werkzeug.exceptions.Unauthorized` exception if
        credentials do not match. If no token is provided, no exception
        will be raised.
    """
    token = request.headers.get("Authorization", None)
    if token is not None and "Bearer" in token:
        auth = User.token_auth(token)
        if auth is None:
            raise Unauthorized()
        else:
            session.update(auth)
            session.authenticated = True
            # This session should not be used to permanently store data
            session.nosave = True


def auth_required():
    """Authentication Required Middleware

    This middleware will force any API user to be authenticated. Note
    that not all endpoints may require authentication.

    :raises: :class:`werkzeug.exceptions.Unauthorized` exception if
        user is not authenticated.
    """
    if not hasattr(session, "authenticated") or not session.authenticated:  # noqa
        raise Unauthorized("You need to login first")


def handle_api_error(error):
    """Handle API Error

    Error handler used for API endpoints

    :returns: JSON Response with error code
    """
    if hasattr(error, "code"):
        error_code = error.code
    else:
        error_code = BadRequest.code
    response = jsonify({"success": False, "error": error.description})
    response.status_code = error_code
    return response


def handle_validation_error(error: ValidationError):
    """Handle API Validation Error

    Error handler for schema validation errors. Most validation errors
    already provide some contextual information about the reason for
    the error itself. This will be returned as a JSON object.

    :returns: JSON response with error code of
        :class:`werkzeug.exceptions.BadRequest`
    """
    if not isinstance(error, ValidationError):
        raise ValueError("Can only handle ValidationError")
    response = jsonify({"success": False, "error": error.normalized_messages()})
    response.status_code = BadRequest.code
    return response


def register(
    parent: Union[Flask, Blueprint], blueprint: Blueprint, auth=False, **kwargs
):
    """Register API Endpoint

    Helper method designed to apply all optional and required
    middlewares to API endpoints.

    :param parent: Current Flask or Blueprint parent instance
    :param blueprint: Blueprint to register as API endpoint
    :param auth: Indicate whether authentication is required. Will add
        the :func:`.auth_required` middleware.
    :param kwargs: Additional arguments passed to
        :meth:`flask.Flask.register_blueprint`
    """
    blueprint.register_error_handler(BadRequest, handle_api_error)
    blueprint.register_error_handler(Unauthorized, handle_api_error)
    blueprint.register_error_handler(ValidationError, handle_validation_error)
    blueprint.before_request(api_auth)
    if auth:
        blueprint.before_request(auth_required)
    parent.register_blueprint(blueprint, **kwargs)


def init_api(app: Flask):
    """Initialize API

    This function will be run inside the :func:`doku.create_app`
    function and initialize the API along all it's endpoints. Any new
    endpoint that should be added to the API has to be registered in
    this function.

    :param app: Current Flask instance
    """
    ###################
    # API v1 Endpoints
    ###################
    register(app, v1.bp, auth=False, url_prefix="/api/v1", name_prefix="api")
    register(
        app, document.bp, auth=True, url_prefix="/api/v1/document", name_prefix="api.v1"
    )
    register(
        app, template.bp, auth=True, url_prefix="/api/v1/template", name_prefix="api.v1"
    )
    register(
        app, variable.bp, auth=True, url_prefix="/api/v1/variable", name_prefix="api.v1"
    )
    register(
        app, vargroup.bp, auth=True, url_prefix="/api/v1/vargroup", name_prefix="api.v1"
    )
    register(
        app,
        stylesheet.bp,
        auth=True,
        url_prefix="/api/v1/stylesheet",
        name_prefix="api.v1",
    )
    register(
        app, resource.bp, auth=True, url_prefix="/api/v1/resource", name_prefix="api.v1"
    )
    register(
        app, snippet.bp, auth=True, url_prefix="/api/v1/snippet", name_prefix="api.v1"
    )
