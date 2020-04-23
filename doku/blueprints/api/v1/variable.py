from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, EXCLUDE
from werkzeug.exceptions import BadRequest

from doku.models import db
from doku.models.document import Variable
from doku.models.schemas import VariableSchema
from doku.utils.db import get_or_404

bp = Blueprint('api.v1.variable', __name__)


@bp.route('/<int:variable_id>', methods=['POST'])
def update(variable_id: int):
    variable: Variable = get_or_404(
        db.session.query(Variable).filter_by(id=variable_id)
    )
    schema = VariableSchema(
        unknown=EXCLUDE, session=db.session,
        instance=variable, partial=True
    )

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    try:
        variable = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    db.session.commit()

    result = schema.dump(variable)
    return jsonify(result)


@bp.route('/', methods=['POST'])
def create():
    schema = VariableSchema(unknown=EXCLUDE, session=db.session)

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    try:
        variable = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    db.session.add(variable)
    db.session.commit()

    result = schema.dump(variable)
    return jsonify(result)


@bp.route('/<int:variable_id>', methods=['DELETE'])
def delete(variable_id: int):
    variable: Variable = get_or_404(
        db.session.query(Variable).filter_by(id=variable_id)
    )
    db.session.delete(variable)
    db.session.commit()
    return jsonify({'success': True})
