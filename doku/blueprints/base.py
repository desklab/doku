from flask import Blueprint, render_template, request

from doku.models import db
from doku.models.document import Document
from doku.utils.decorators import login_required
from doku.utils.db import get_pagination_page, get_ordering

bp = Blueprint("base", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    page = get_pagination_page()
    ordering, order, direction = get_ordering(
        Document, default_order="last_updated", default_dir="desc"
    )
    query: str = request.args.get("query", "", type=str)
    documents = db.session.query(Document)
    if query != "":
        documents = documents.filter(Document.__ts_vector__.match(query))
    documents = documents.order_by(ordering).paginate(page=page, per_page=10)
    return render_template(
        "sites/index.html",
        documents=documents,
        order=order,
        direction=direction,
        query=query,
    )
