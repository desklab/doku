import json
from datetime import datetime

from celery.result import AsyncResult
from flask import Blueprint, current_app, jsonify, request, session
from flask_babel import format_timedelta, format_datetime
from werkzeug.exceptions import BadRequest, TooManyRequests

from doku.blueprints.api.v1.base import api_view_factory
from doku.models import db
from doku.models.document import Document
from doku.models.schemas import DocumentSchema
from doku.tasks import celery
from doku.tasks.download import request_download
from doku.utils import EMPTY

bp = Blueprint("document", __name__)


DocumentApiView = api_view_factory(
    Document, DocumentSchema,
    register=True, register_args=(bp, "api", "/")
)


@bp.route("/ids", methods=["GET"])
def get_ids():
    ids = [__id[0] for __id in db.session.query(Document.id).distinct().all()]
    return jsonify({"result": ids})


@bp.route("/download/request", methods=["POST"])
def download():
    """Bulk Download Request

    Request compilation of multiple documents

    Request data could container either be a boolean field ``all`` or
    a list of document IDs that should be excluded ``exclude`` or
    included ``include``.
    """
    user_id = session.get("id", None)
    if user_id is None:
        raise BadRequest()
    limit = current_app.config.get("PENDING_DOWNLOAD_LIMIT", 5)
    downloads = get_downloads_for_user(user_id)
    if len(downloads) >= limit:
        raise TooManyRequests(f"You have {len(downloads)} pending downloads.")
    r = current_app.redis
    download_all = request.json.get("all", False)
    include = request.json.get("include")
    exclude = request.json.get("exclude")
    task = request_download.apply_async(args=(download_all, include, exclude))
    tasks = r.get(f"doku_downloads_user_{user_id:d}")
    if tasks in EMPTY:
        tasks = {}
    else:
        tasks = json.loads(tasks)
    if tasks in EMPTY:
        tasks = {}
    tasks[task.id] = datetime.now().isoformat()
    r.set(f"doku_downloads_user_{user_id:d}", json.dumps(tasks))
    return jsonify({"success": True, "id": task.id})


@bp.route("/download/requests", methods=["GET"])
def get_downloads():
    user_id = session.get("id", None)
    if user_id is None:
        raise BadRequest()
    res = get_downloads_for_user(user_id)
    return jsonify({"result": res})


def get_downloads_for_user(user_id: int) -> dict:
    r = current_app.redis
    tasks = r.get(f"doku_downloads_user_{user_id:d}")
    if tasks in EMPTY:
        return {}
    tasks = json.loads(tasks)
    if tasks in EMPTY:
        return {}
    downloads = {}
    for task_id, date in tasks.items():
        result = AsyncResult(task_id, app=celery)
        _date = datetime.fromisoformat(date)
        downloads[task_id] = {
            "status": result.status,
            "date": _date,
            "timedelta": format_timedelta(datetime.now() - _date),
            "date_format": format_datetime(_date),
        }
    return downloads
