import os
from io import BytesIO

from flask import (
    Blueprint,
    render_template,
    send_file,
    request,
    flash,
    current_app,
    send_from_directory,
)
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from doku import db
from doku.models.template import Stylesheet
from doku.utils.db import get_or_404, get_pagination_page
from doku.utils.decorators import login_required
from doku.models.schemas.template import StylesheetSchema

bp = Blueprint("stylesheets", __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if request.values.get("name", None) is not None:
            name = request.values.get("name")
        else:
            flash("No name provided")
            raise BadRequest("No name provided")

        if request.files.get("file", None) is not None:
            file: FileStorage = request.files.get("file")
            source = file.read().decode(encoding="UTF-8", errors="strict")
            file.close()
        else:
            flash("No file provided")
            raise BadRequest("No file provided")

        if name is not None and source is not None:
            stylesheet = Stylesheet(name=name, source=source)
            db.session.add(stylesheet)
            db.session.commit()

    page = get_pagination_page()
    query: str = request.args.get("query", "", type=str)
    stylesheets = db.session.query(Stylesheet)
    if query != "":
        stylesheets = stylesheets.filter(Stylesheet.__ts_vector__.match(query))
    stylesheets = stylesheets.paginate(page=page, per_page=10)

    stylesheet_schemas = StylesheetSchema(
        session=db.session, many=True, include=("source",)
    )
    return render_template(
        "sites/stylesheets.html",
        stylesheets_json=stylesheet_schemas.dumps(stylesheets.items),
        stylesheets=stylesheets, query=query
    )
