import os

from marshmallow_sqlalchemy import auto_field
from marshmallow import fields, validate
from flask import jsonify, current_app

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
