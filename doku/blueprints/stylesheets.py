from io import BytesIO
import os

from flask import (
    Blueprint,
    render_template,
    send_file,
    request,
    flash,
    current_app,
    send_from_directory,
)

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
    page = get_pagination_page()
    stylesheets = db.session.query(Stylesheet).paginate(page=page, per_page=10)

    stylesheet_schemas = StylesheetSchema(session=db.session, many=True)
    return render_template(
        "sites/stylesheets.html",
        stylesheets_json=stylesheet_schemas.dumps(stylesheets.items),
        stylesheets=stylesheets
    )
