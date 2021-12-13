from flask import Blueprint

from doku.models.schemas import VariableGroupSchema

bp = Blueprint("vargroup", __name__)


@bp.route("/", methods=["GET"])
def get_all():
    return VariableGroupSchema.get_all()


@bp.route("/<int:vargroup_id>/", methods=["GET"])
def get(vargroup_id: int):
    return VariableGroupSchema.get(vargroup_id)


@bp.route("/", methods=["PUT", "PATCH"])
def update():
    return VariableGroupSchema.update()


@bp.route("/", methods=["POST"])
def create():
    return VariableGroupSchema.create()


@bp.route("/<int:vargroup_id>/", methods=["DELETE"])
def delete(vargroup_id: int):
    return VariableGroupSchema.delete(vargroup_id)
