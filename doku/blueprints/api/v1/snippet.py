from flask import Blueprint
from doku.models.schemas import SnippetSchema


bp = Blueprint("api.v1.snippet", __name__)


@bp.route("/", methods=["POST"])
def create():
    return SnippetSchema.create(commit=True)


@bp.route("/", methods=["PUT", "PUSH"])
def update():
    return SnippetSchema.update()


@bp.route("/", methods=["GET"])
def get_all():
    return SnippetSchema.get_all()


@bp.route("/<int:snippet_id>/", methods=["GET"])
def get(snippet_id: int):
    return SnippetSchema.get(snippet_id)


@bp.route("/<int:snippet_id>/", methods=["DELETE"])
def delete(snippet_id: int):
    return SnippetSchema.delete(snippet_id)
