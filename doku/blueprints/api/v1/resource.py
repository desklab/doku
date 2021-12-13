from flask import Blueprint

from doku.models.schemas import ResourceSchema
from doku.utils.decorators import login_required

bp = Blueprint("resource", __name__)


@bp.route("/", methods=["POST"])
def create():
    raise NotImplementedError()


@bp.route("/", methods=["PUT", "PATCH"])
def update():
    return ResourceSchema.update()


@bp.route("/", methods=["GET"])
def get_all():
    return ResourceSchema.get_all()


@bp.route("/<int:resource_id>/", methods=["GET"])
def get(resource_id: int):
    return ResourceSchema.get(resource_id)


@bp.route("/<int:resource_id>/", methods=["DELETE"])
def delete(resource_id: int):
    return ResourceSchema.delete(resource_id)
