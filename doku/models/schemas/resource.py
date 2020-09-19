from marshmallow_sqlalchemy import auto_field
from marshmallow import fields, validate
from flask import jsonify, current_app
import os

from doku.models import DateSchemaMixin
from doku.models.resource import Resource
from doku.models.schemas.common import DokuSchema, ApiSchema, NotEmptyString
from doku.utils.db import get_or_404
from doku import db


class ResourceSchema(ApiSchema, DateSchemaMixin):
    class Meta:
        model = Resource
        load_instance = True

    API_NAME = "resource"

    id = auto_field()
    name = NotEmptyString()
    filename = auto_field()
    url = fields.String(dump_only=True)

    @classmethod
    def delete(cls, instance_id: int, commit=True):
        instance = get_or_404(
            db.session.query(cls.Meta.model).filter_by(id=instance_id)
        )
        filename = instance.filename
        os.remove(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        db.session.delete(instance)
        if commit:
            db.session.commit()

        return jsonify({"success": True})
