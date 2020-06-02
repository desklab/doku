from flask import Blueprint

from doku.models.schemas.resource import ResourceSchema
from doku.utils.decorators import login_required

bp = Blueprint("api.v1.resource", __name__)


@bp.before_request
@login_required
def login_check():
    pass


@bp.route("/", methods=["POST"])
def create():
    return ResourceSchema.create()


@bp.route("/", methods=["PUT"])
def update():
    return ResourceSchema.update()


@bp.route("/", methods=["GET"])
def get_all():
    return ResourceSchema.get_all()


@bp.route("/<int:document_id>/", methods=["GET"]) #TODO: is document_id correct?
def get(document_id: int):
    return ResourceSchema.get(document_id)


@bp.route("/<int:document_id>/", methods=["DELETE"]) #TODO: is document_id correct?
def delete(document_id: int):
    return ResourceSchema.delete(document_id)
