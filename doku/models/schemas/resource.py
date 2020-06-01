from marshmallow_sqlalchemy import auto_field
from marshmallow import fields

from doku.models import DateSchemaMixin
from doku.models.resource import Resource
from doku.models.schemas.common import DokuSchema, ApiSchemaMixin


class ResourceSchema(DokuSchema, DateSchemaMixin, ApiSchemaMixin):
    class Meta:
        model = Resource
        load_instance = True

    API_NAME = "resource"

    id = auto_field()
    name = auto_field()
    filename = auto_field()
    url = fields.String(dump_only=True)
