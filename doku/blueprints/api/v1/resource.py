from flask import Blueprint

from doku.models.schemas.resource import ResourceSchema
from doku.utils.decorators import login_required

bp = Blueprint("api.v1.resource", __name__)


@bp.before_request
@login_required
def login_check():
    pass

@bp.route("/upload/<int:resource_id>", methods=["PUT"])
def upload(resource_id: int):
    resource: Resource = get_or_404(
        db.session.query(Resource).filter_by(id=resource_id)
    )
    schema = ResourceSchema(
        unknown=EXCLUDE, session=db.session, instance=resource, partial=True
    )

    data = dict(request.form.copy())
    if request.json is not None:
        data.update(request.json)

    if request.files.get("source", None) is not None:
        file: FileStorage = request.files.get("source")
        data["source"] = file.read()
        file.close()

    try:
        resource = schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), BadRequest.code

    db.session.commit()

    result = schema.dump(resource)
    return jsonify(result)

@bp.route("/", methods=["POST"])
def create():
    return ResourceSchema.create()

@bp.route("/", methods=["PUT"])
def update():
    return ResourceSchema.update()

@bp.route("/", methods=["GET"])
def get_all():
    return ResourceSchema.get_all()


@bp.route("/<int:resource_id>/", methods=["GET"])
def get(resource_id: int):
    return ResourceSchema.get(resource_id)


@bp.route("/<int:resource_id>/", methods=["DELETE"])
def delete(resource_id: int):
    return ResourceSchema.delete(resource_id)
