from flask import Blueprint, jsonify

from doku import db
from doku.models.schemas import TemplateSchema, StylesheetSchema
from doku.models.template import Template, Stylesheet
from doku.utils.db import get_or_404

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


@bp.route('/<int:template_id>/stylesheet', methods=['POST'])
def add_stylesheet(template_id: int):
    template: Template = get_or_404(
        db.session.query(Template).filter_by(id=template_id)
    )
    template_schema = TemplateSchema(include=('styles',))
    data = TemplateSchema.all_request_data()
    if isinstance(data, list):
        for entry in data:
            style: Stylesheet = get_or_404(
                db.session.query(Stylesheet).filter_by(**entry)
            )
            template.styles.append(style)
    else:
        style: Stylesheet = get_or_404(
            db.session.query(Stylesheet).filter_by(**data)
        )
        template.styles.append(style)
    db.session.commit()
    return jsonify(template_schema.dumps(template))
