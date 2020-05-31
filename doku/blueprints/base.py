from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound
from flask import Blueprint, session, redirect, url_for, request, render_template

from doku import db
from doku.models.document import Document
from doku.utils.decorators import login_required


bp = Blueprint("base", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    documents = db.session.query(Document).all()
    return render_template("sites/index.html", documents=documents)
