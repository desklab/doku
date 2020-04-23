from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, EXCLUDE
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from doku.models import db
from doku.models.document import Variable
from doku.models.schemas import DocumentSchema, TemplateSchema, StylesheetSchema
from doku.models.template import Template, Stylesheet
from doku.utils.db import get_or_404, get_or_create

bp = Blueprint('api.v1.stylesheet', __name__)


@bp.route('/<int:stylesheet_id>', methods=['PUT'])
def update(stylesheet_id: int):
    style: Stylesheet = get_or_404(
        db.session.query(Stylesheet).filter_by(id=stylesheet_id)
    )
    schema = StylesheetSchema(unknown=EXCLUDE, session=db.session,
                              instance=style, partial=True)

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    if request.files.get('source', None) is not None:
        file: FileStorage = request.files.get('source')
        data['source'] = file.read()
        file.close()

    try:
        stylesheet = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    db.session.commit()

    result = schema.dump(stylesheet)
    return jsonify(result)
