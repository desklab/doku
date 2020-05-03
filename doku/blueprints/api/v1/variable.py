from flask import Blueprint

from doku.models.schemas import VariableSchema
from doku.utils.decorators import login_required

bp = Blueprint('api.v1.variable', __name__)


@bp.before_request
@login_required
def login_check():
    pass


@bp.route('/', methods=['GET'])
def get_all():
    return VariableSchema.get_all()


@bp.route('/<int:variable_id>/', methods=['GET'])
def get(variable_id: int):
    return VariableSchema.get(variable_id)


@bp.route('/', methods=['PUT'])
def update():
    return VariableSchema.update()


@bp.route('/', methods=['POST'])
def create():
    return VariableSchema.create()


@bp.route('/<int:variable_id>/', methods=['DELETE'])
def delete(variable_id: int):
    return VariableSchema.delete(variable_id)
