from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, EXCLUDE
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from doku.blueprints.api.v1.base import api_view_factory
from doku.models import db
from doku.models.schemas import StylesheetSchema
from doku.models.template import Stylesheet
from doku.utils.db import get_or_404

bp = Blueprint("stylesheet", __name__)


@bp.route("/upload/<int:stylesheet_id>", methods=["PUT", "PATCH"])
def upload(stylesheet_id: int):
    style: Stylesheet = get_or_404(
        db.session.query(Stylesheet).filter_by(id=stylesheet_id)
    )
    schema = StylesheetSchema(
        unknown=EXCLUDE,
        session=db.session,
        instance=style,
        partial=True,
        include=("source",),
    )

    data = dict(request.form.copy())
    if request.get_json(silent=True) is not None:
        data.update(request.get_json(silent=True))

    if request.files.get("source", None) is not None:
        file: FileStorage = request.files.get("source")
        data["source"] = file.read()
        file.close()

    try:
        stylesheet = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    db.session.commit()

    result = schema.dump(stylesheet)
    return jsonify(result)


StylesheetApiView = api_view_factory(
    Stylesheet, StylesheetSchema,
    register=True, register_args=(bp, "api", "/")
)
