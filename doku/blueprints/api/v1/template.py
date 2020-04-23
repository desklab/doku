from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, EXCLUDE
from werkzeug.exceptions import BadRequest

from doku.models import db
from doku.models.document import Variable
from doku.models.schemas import DocumentSchema, TemplateSchema
from doku.models.template import Template, Stylesheet
from doku.utils.db import get_or_404, get_or_create

bp = Blueprint('api.v1.template', __name__)


@bp.route('/<int:template_id>', methods=['PUT'])
def update(template_id: int):
    template: Template = get_or_404(
        db.session.query(Template).filter_by(id=template_id)
    )
    schema = TemplateSchema(unknown=EXCLUDE, session=db.session,
                            instance=template, partial=True)

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    try:
        template = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    for document in template.documents:
        for name in template.available_fields:
            get_or_create(Variable, document=document, name=name)

    db.session.commit()

    result = schema.dump(template)
    return jsonify(result)


@bp.route('/', methods=['GET'])
def get():
    page = request.args.get('page')
    schemas = TemplateSchema(unknown=EXCLUDE, session=db.session, many=True)
    templates = Template.query.paginate(page=page, per_page=25).items
    result = schemas.dump(templates)
    return jsonify(result)
