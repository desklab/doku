from flask import Blueprint

from doku.models.schemas import DocumentSchema
from doku.utils.decorators import login_required

bp = Blueprint('api.v1.document', __name__)


@bp.before_request
@login_required
def login_check():
    pass


@bp.route('/', methods=['POST'])
def create():
    return DocumentSchema.create(commit=True)


@bp.route('/', methods=['PUT'])
def update():
    return DocumentSchema.update()


@bp.route('/', methods=['GET'])
def get_all():
    return DocumentSchema.get_all()


@bp.route('/<int:document_id>/', methods=['GET'])
def get(document_id: int):
    return DocumentSchema.get(document_id)


@bp.route('/<int:document_id>/', methods=['DELETE'])
def delete(document_id: int):
    return DocumentSchema.delete(document_id)
