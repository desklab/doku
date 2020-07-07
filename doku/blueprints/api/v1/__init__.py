from werkzeug.exceptions import BadRequest, Unauthorized
from flask import Blueprint, jsonify, request, session

from doku.models.user import User
from doku.utils.middlewares.csrf import csrf

bp = Blueprint("api.v1", __name__)


@bp.route("/heartbeat", methods=["GET"])
def dashboard():
    return jsonify({"status": "healthy"})


@bp.route("/login", methods=["POST"])
@csrf.exempt
def login():
    if request.authorization is None:
        raise BadRequest("No authorization provided")
    email = request.authorization.get("username")
    password = request.authorization.get("password")
    user = User.authenticate(email=email, password=password)
    if user is None:
        raise Unauthorized("E-Mail and password do not match. Please try again")
    else:
        session.authenticated = True
        session.update({
            "user": user.username,
            "id": user.id,
            "name": user.name
        })
        return jsonify({
            "success": True,
            "token_type": "Bearer",
            "access_token": user.token.get("token"),
            "expires_in": user.token.get("expires_in")
        })
