from functools import wraps

from werkzeug.exceptions import Unauthorized
from flask import session, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(session, "authenticated") or not session.authenticated:
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.authenticated:
            raise Unauthorized("You need to login first")
        return f(*args, **kwargs)

    return decorated_function
