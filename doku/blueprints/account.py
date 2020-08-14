import json
import os
import shutil
from typing import Optional

from celery.result import AsyncResult
from celery.states import SUCCESS
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, BadRequest
from werkzeug.security import safe_join
from flask import Blueprint, session, redirect, url_for, request, \
    render_template, flash, current_app, send_file

from doku.models import db
from doku.models.user import User
from doku.blueprints.api.v1.document import get_downloads_for_user
from doku.utils.decorators import login_required
from doku.tasks import celery

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
    user_id = session.get("id", None)
    if user_id is None:
        raise BadRequest()
    res = get_downloads_for_user(user_id)
    return render_template("sites/account/download.html", downloads=res)


@bp.route("/downloads/download/<string:download_id>", methods=["GET"])
@login_required
def download(download_id: str):
    user_id = session.get("id", None)
    if user_id is None:
        raise BadRequest()
    res = get_downloads_for_user(user_id)
    if download_id not in res:
        return NotFound(f"Unknown download ID {download_id}")
    result = AsyncResult(download_id, app=celery)
    if result.status != SUCCESS:
        return BadRequest(f"Not ready for download")
    filename = result.get()
    file = safe_join(current_app.config.get("SHARED_FOLDER"), filename)
    if not os.path.exists(file) and not os.path.isfile(file):
        raise RuntimeError(f"Return value {filename} of task does not denote"
                           f" to file ({file})")
    return send_file(
        file,
        as_attachment=True,
        attachment_filename=filename,
        mimetype="application/zip",
        cache_timeout=0,
    )


@bp.route("/downloads/delete", methods=["POST"])
@login_required
def downloads_delete():
    user_id = session.get("id", None)
    if user_id is None:
        raise BadRequest()
    res = get_downloads_for_user(user_id)
    download_id = request.form.get("download_id", None)
    if download_id not in res:
        return BadRequest(f"Unknown download ID {download_id}")
    result = AsyncResult(download_id, app=celery)
    try:
        shared_folder = current_app.config.get("SHARED_FOLDER")
        shutil.rmtree(safe_join(shared_folder, download_id))
    except:
        pass
    if result.status == SUCCESS:
        filename = result.get()
        file = safe_join(current_app.config.get("SHARED_FOLDER"), filename)
        if os.path.exists(file):
            os.remove(file)
    result.revoke()
    result.forget()
    del res[download_id]
    r = current_app.redis
    new_tasks = {
        task_id: val["date"].isoformat() for task_id, val in res.items()
    }
    r.set(f"doku_downloads_user_{user_id:d}", json.dumps(new_tasks))
    return redirect(url_for("account.downloads"))


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
