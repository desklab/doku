from flask import Blueprint, jsonify


bp = Blueprint("api.v1", __name__)


@bp.route("/heartbeat", methods=["GET"])
def dashboard():
    return jsonify({"status": "healthy"})
