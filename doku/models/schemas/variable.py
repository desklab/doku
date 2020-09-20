import string

from marshmallow import fields
from marshmallow.validate import ContainsOnly
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested

from doku.models import DateSchemaMixin
from doku.models.schemas.common import DokuSchema, ApiSchema, NotEmptyString
from doku.models.variable import VariableGroup, Variable


VALID_VARIABLE_CHARACTERS = f"{string.ascii_letters}{string.digits}_"
VARIABLE_NAME_ERROR = "{input} is not a valid variable name."


class VariableSchema(ApiSchema, DateSchemaMixin):
    class Meta:
        model = Variable
        load_instance = True

    API_NAME = "variable"

    id = auto_field()
    name = NotEmptyString(
        validate=ContainsOnly(VALID_VARIABLE_CHARACTERS, error=VARIABLE_NAME_ERROR)
    )
    use_markdown = auto_field()
    css_class = auto_field()
    content = auto_field()
    compiled_content = auto_field(dump_only=True)
    document_id = auto_field(load_only=True)
    parent_id = auto_field(load_only=True)
    snippet_id = auto_field(load_only=True)
    group_id = auto_field(load_only=True)

    parent = Nested("VariableSchema", allow_none=True, exclude=("children",))
    document = Nested("DocumentSchema", exclude=("variables",), dump_only=True)
    children = Nested("VariableSchema", exclude=("parent",), many=True, partial=True)
    snippet = Nested("SnippetSchema", exclude=("used_by",), many=False, partial=True)
    group = Nested("VariableGroupSchema", exclude=("variables", "document"))

    used = fields.Boolean(dump_only=True)
    is_list = fields.Boolean(dump_only=True)
    uses_snippet = fields.Boolean(dump_only=True)


class VariableGroupSchema(ApiSchema):
    class Meta:
        model = VariableGroup
        load_instance = True

    API_NAME = "vargroup"

    id = auto_field()
    name = NotEmptyString()

    document_id = auto_field(load_only=True)

    variables = Nested(VariableSchema, allow_none=True, exclude=("group", "document"), many=True)
    document = Nested("DocumentSchema", exclude=("variable_groups",), dump_only=True)
