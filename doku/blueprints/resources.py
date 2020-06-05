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

from doku import db
from doku.models.resource import Resource, generate_filename
from doku.utils.db import get_or_404
from doku.utils.decorators import login_required
from doku.models.schemas.resource import ResourceSchema

bp = Blueprint("resources", __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        print(request.files)
        if "file" not in request.files:
            flash("No file provided")
        else:
            file = request.files["file"]
            if file.filename == "":
                flash("No file provided")
            else:
                filename = generate_filename(file.filename)
                name = request.values.get("name", filename)
                resource = Resource(name=name, filename=filename)
                dest = current_app.config["UPLOAD_FOLDER"]
                file.save(os.path.join(dest, filename))
                db.session.add(resource)
                db.session.commit()
    resources = db.session.query(Resource).all()

    resource_schemas = ResourceSchema(session=db.session, many=True)
    return render_template(
        "sites/resources.html",
        resources_json=resource_schemas.dumps(resources),
    )


@bp.route("/view/<int:resource_id>", methods=["GET"])
@login_required
def view(resource_id: int):
    resource: Resource = get_or_404(
        db.session.query(Resource).filter_by(id=resource_id)
    )
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], resource.filename)
