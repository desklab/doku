import json

from werkzeug.exceptions import BadRequest, TooManyRequests
from flask import Blueprint, current_app, jsonify, request, session
from celery.result import AsyncResult

from doku.models.schemas import DocumentSchema
from doku.tasks import celery
from doku.utils import EMPTY

bp = Blueprint("api.v1.document", __name__)


@bp.route("/", methods=["POST"])
def create():
    return DocumentSchema.create(commit=True)


@bp.route("/", methods=["PUT"])
def update():
    return DocumentSchema.update()


@bp.route("/", methods=["GET"])
def get_all():
    return DocumentSchema.get_all()


@bp.route("/<int:document_id>/", methods=["GET"])
def get(document_id: int):
    return DocumentSchema.get(document_id)


@bp.route("/<int:document_id>/", methods=["DELETE"])
def delete(document_id: int):
    return DocumentSchema.delete(document_id)


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
    download_all = request.args.get("all", False, type=bool)
    include = request.args.getlist("include", type=int)
    exclude = request.args.getlist("exclude", type=int)
    task = request_download.apply_async(args=(download_all, include, exclude))
    tasks = r.get(f"doku_downloads_user_{user_id:d}")
    if tasks in EMPTY:
        tasks = []
    else:
        tasks = json.loads(tasks)
    tasks.append(task.id)
    r.set(f"doku_downloads_user_{user_id:d}", json.dumps(tasks))
    return jsonify({"success": True, "id": task.id})


@bp.route("/download/requests", methods=["GET"])
def get_downloads():
    user_id = session.get("id", None)
    if user_id is None:
        raise BadRequest()
    res = get_downloads_for_user(user_id)
    return jsonify(res)


def get_downloads_for_user(user_id: int) -> dict:
    r = current_app.redis
    tasks = r.get(f"doku_downloads_user_{user_id:d}")
    print(tasks)
    if tasks in EMPTY:
        return {}
    tasks = json.loads(tasks)
    downlaods = {}
    for task_id in tasks:
        result = AsyncResult(task_id, app=celery)
        downlaods[task_id] = result.status
    return downlaods
