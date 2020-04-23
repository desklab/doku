from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, EXCLUDE
from werkzeug.exceptions import BadRequest

from doku.models import db
from doku.models.document import Document, Variable
from doku.models.schemas import DocumentSchema
from doku.models.template import Template, Stylesheet, DEFAULT_TEMPLATE
from doku.utils.db import get_or_404, get_or_create

bp = Blueprint('api.v1.document', __name__)


@bp.route('/', methods=['POST'])
def create():
    schema = DocumentSchema(unknown=EXCLUDE, session=db.session)

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    try:
        document = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    if document.template_id is None:
        template = Template(name=f'{document.name} - Template')
        template.source = DEFAULT_TEMPLATE
        stylesheet = Stylesheet(name=f'{document.name} - Styles')
        template.base_style = stylesheet
        document.template = template
        db.session.add(stylesheet)
        db.session.add(template)

    for name in document.template.available_fields:
        variable = Variable(document=document, name=name)
        db.session.add(variable)

    db.session.add(document)
    db.session.commit()

    result = schema.dump(document)
    return jsonify(result)


@bp.route('/<int:document_id>', methods=['POST', 'PUT'])
def update(document_id: int):
    document: Document = get_or_404(
        db.session.query(Document).filter_by(id=document_id)
    )
    schema = DocumentSchema(unknown=EXCLUDE, session=db.session,
                            instance=document, partial=True)

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    try:
        document = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    for name in document.template.available_fields:
        get_or_create(Variable, document=document, name=name)

    db.session.commit()

    result = schema.dump(document)
    return jsonify(result)
