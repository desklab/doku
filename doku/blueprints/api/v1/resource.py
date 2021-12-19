import os
import typing as t

from flask import Blueprint, current_app, jsonify

from doku.blueprints.api.v1.base import BaseApiView
from doku.models import db
from doku.models.resource import Resource
from doku.models.schemas import ResourceSchema
from doku.models.schemas.common import ApiSchema

bp = Blueprint("resource", __name__)


class ResourceApiView(BaseApiView):
    model: t.Type[db.Model] = Resource
    schema: t.Type[ApiSchema] = ResourceSchema

    def post(self, *, commit: bool = True):
        raise NotImplementedError()

    def delete(self, pk: int, commit: bool = True):
        instance = self.get_instance(pk)
        filename = instance.filename
        os.remove(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        db.session.delete(instance)
        if commit:
            db.session.commit()
        return jsonify({"success": True})


ResourceApiView.register(bp, "api", "/")
