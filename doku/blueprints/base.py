from sqlalchemy import text, desc, asc
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound
from flask import Blueprint, session, redirect, url_for, request, render_template

from doku import db
from doku.models.document import Document
from doku.utils.decorators import login_required
from doku.utils.db import get_pagination_page


bp = Blueprint("base", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    page = get_pagination_page()
    order = request.args.get("order", "last_updated")
    direction = request.args.get("dir", "desc")
    direc = desc
    if direction == "asc":
        direc = asc
    if order is not None and hasattr(Document, order):
        documents = (
            db.session.query(Document)
            .order_by(direc(text(order)))
            .paginate(page=page, per_page=10)
        )
    else:
        documents = db.session.query(Document).paginate(page=page, per_page=10)
    return render_template(
        "sites/index.html", documents=documents, order=order, direction=direction
    )
