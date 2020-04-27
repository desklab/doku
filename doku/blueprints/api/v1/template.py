from flask import Blueprint

from doku.models.schemas import TemplateSchema

bp = Blueprint('api.v1.template', __name__)


@bp.route('/', methods=['PUT'])
def update():
    return TemplateSchema.update()


@bp.route('/', methods=['POST'])
def create():
    return TemplateSchema.create()


@bp.route('/', methods=['GET'])
def get_all():
    return TemplateSchema.get_all()


@bp.route('/<int:template_id>/', methods=['GET'])
def get(template_id: int):
    return TemplateSchema.get(template_id)


@bp.route('/<int:template_id>/', methods=['DELTE'])
def delete(template_id: int):
    return TemplateSchema.delete(template_id)
