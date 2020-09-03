from flask import Blueprint, render_template

from doku import db
from doku.models.schemas import SnippetSchema
from doku.models.snippet import Snippet
from doku.utils.db import get_pagination_page, get_ordering, get_or_404
from doku.utils.decorators import login_required

bp = Blueprint("snippet", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    page = get_pagination_page()
    snippets = (
        db.session.query(Snippet).paginate(page=page, per_page=10)
    )
    return render_template("sites/snippets.html", snippets=snippets)


@bp.route("/<int:snippet_id>", methods=["GET", "POST"])
@login_required
def get(snippet_id: int):
    snippet = get_or_404(db.session.query(Snippet).filter_by(id=snippet_id))
    snippet_schema = SnippetSchema(session=db.session, instance=snippet)
    return render_template(
        "sites/snippet_edit.html",
        snippet=snippet,
        snippet_json=snippet_schema.dump(snippet)
    )
