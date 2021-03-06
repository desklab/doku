from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested

from doku.models import DateSchemaMixin
from doku.models.schemas.common import DokuSchema, ApiSchema, NotEmptyString
from doku.models.snippet import Snippet


class SnippetSchema(ApiSchema, DateSchemaMixin):
    class Meta:
        model = Snippet
        load_instance = True

    API_NAME = "snippet"

    id = auto_field()
    name = NotEmptyString()

    use_markdown = auto_field()
    css_class = auto_field()

    content = auto_field()
    compiled_content = auto_field(dump_only=True)

    used_by = Nested("VariableSchema", dump_only=True, only=("name", "id", "document"))
