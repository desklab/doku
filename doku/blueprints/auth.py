from typing import Optional

from flask import Blueprint, session, redirect, url_for, request, render_template
from werkzeug.exceptions import Unauthorized

from doku.models.user import User
from doku.utils.decorators import login_required

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.authenticated:
        return redirect(url_for("base.index"))
    error: Optional[str] = None
    email = None
    error_code = 200
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.authenticate(email=email, password=password)
        if user is None:
            error_code = Unauthorized.code
            error = "E-Mail and password do not match. Please try again"
        else:
            session.authenticated = True
            session.update({"user": user.username, "id": user.id, "name": user.name})
            return redirect(url_for("base.index"))
    return (
        render_template("sites/auth/login.html", error=error, email=email),
        error_code,
    )


@bp.route("/logout")
@login_required
def logout():
    session.authenticated = False
    return redirect(url_for("base.index"))
