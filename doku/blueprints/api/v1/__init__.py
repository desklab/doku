from werkzeug.exceptions import Unauthorized, Forbidden, NotFound
from flask import Blueprint, session, redirect, url_for, request, render_template

from doku.models import db
from doku.models.user import User
from doku.utils.decorators import login_required


bp = Blueprint('api.v1', __name__)


@bp.route('/', methods=['GET'])
@login_required
def dashboard():
    return NotFound('Not Implemented')
