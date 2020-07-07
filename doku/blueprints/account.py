from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, BadRequest
from flask import Blueprint, session, redirect, url_for, request, render_template, flash

from doku.models import db
from doku.models.user import User
from doku.utils.decorators import login_required

bp = Blueprint("account", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    return render_template("sites/account/index.html")


@bp.route("/security", methods=["GET"])
@login_required
def security():
    return render_template("sites/account/security.html")


@bp.route("/downloads", methods=["GET"])
@login_required
def downloads():
    return render_template("sites/account/index.html")


@bp.route("/security/password", methods=["POST"])
@login_required
def security_change_password():
    old_password = request.form.get("password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("rpt_password")
    if not new_password == confirm_password:
        return (
            render_template(
                "sites/account/security.html", error_new="Passwords don't match"
            ),
            BadRequest.code,
        )
    user = db.session.query(User).filter_by(username=session["user"]).one()
    if not user.check_password(old_password):
        return (
            render_template(
                "sites/account/security.html", error_old="Invalid password"
            ),
            BadRequest.code,
        )
    user.set_password(new_password)
    db.session.commit()
    flash("Password changed successfully")
    return redirect(url_for("account.security"))
