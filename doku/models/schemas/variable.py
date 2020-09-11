from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested

from doku.models import DateSchemaMixin
from doku.models.schemas.common import DokuSchema, ApiSchema, NotEmptyString
from doku.models.variable import VariableGroup


class VariableGroupSchema(ApiSchema):
    class Meta:
        model = VariableGroup
        load_instance = True

    API_NAME = "vargroup"

    id = auto_field()
    name = NotEmptyString()

    document_id = auto_field(load_only=True)

    variables = Nested("VariableSchema", allow_none=True, exclude=("group", "document"), many=True)
    document = Nested("DocumentSchema", exclude=("variable_groups",), dump_only=True)
