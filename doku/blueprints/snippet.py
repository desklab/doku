from flask import Blueprint, render_template, request, flash, redirect, url_for
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

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
    error_messages = {}
    snippet = get_or_404(db.session.query(Snippet).filter_by(id=snippet_id))
    snippet_schema = SnippetSchema(session=db.session, instance=snippet)
    if request.method == "POST":
        data = request.form.copy()
        data["id"] = snippet_id
        # Partial data is disabled as all attributes should be provided.
        # Even the id is given by the url itself.
        # This helps us catch issues when form data is missing.
        try:
            snippet = snippet_schema.load(data, instance=snippet, partial=False)
            db.session.commit()
        except ValidationError as e:
            error_messages = e.messages
            for error in error_messages.values():
                flash(", ".join(error))
    return render_template(
        "sites/snippet_edit.html",
        snippet=snippet,
        snippet_json=snippet_schema.dump(snippet),
        error_messages=error_messages
    ), BadRequest.code if error_messages != {} else 200


@bp.route("/create", methods=["POST"])
@login_required
def create_snippet():
    snippet = Snippet()
    snippet.name = "New Snippet"
    db.session.add(snippet)
    db.session.commit()
    return redirect(url_for("snippet.get", snippet_id=snippet.id))
