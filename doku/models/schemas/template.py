from typing import Optional

from flask import url_for, jsonify
from marshmallow import fields, ValidationError
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from werkzeug.exceptions import BadRequest

from doku.models import DateSchemaMixin, db
from doku.models.schemas.common import ApiSchema, NotEmptyString
from doku.models.template import Template, Stylesheet
from doku.models.variable import Variable
from doku.utils.db import get_or_create, get_or_404
from doku.utils.jinja import validate_template


class TemplateSchema(ApiSchema, DateSchemaMixin):
    class Meta:
        model = Template
        exclude = ("documents",)
        load_instance = True

    API_NAME = "template"

    id = auto_field()
    name = NotEmptyString()
    source = auto_field(validate=validate_template)
    documents = Nested("DocumentSchema", many=True, exclude=("template",))
    styles = Nested("StylesheetSchema", many=True, exclude=("templates",))
    available_fields = fields.List(fields.String, dump_only=True)
    add_styles_url = fields.Method("_add_styles_url", dump_only=True, allow_none=True)
    remove_styles_url = fields.Method(
        "_remove_styles_url", dump_only=True, allow_none=True
    )

    def _add_styles_url(self, template) -> Optional[str]:
        if template.id is None:
            return None
        return url_for("api.v1.template.add_stylesheet", template_id=template.id)

    def _remove_styles_url(self, template) -> Optional[str]:
        if template.id is None:
            return None
        return url_for("api.v1.template.remove_stylesheet", template_id=template.id)


class StylesheetSchema(ApiSchema, DateSchemaMixin):
    class Meta:
        model = Stylesheet
        exclude = ("source",)
        load_instance = True

    API_NAME = "stylesheet"

    id = auto_field()
    name = NotEmptyString()
    source = fields.String()
    templates = Nested("TemplateSchema", exclude=("styles",), many=True)

    upload_url = fields.Method("_upload_url", dump_only=True, allow_none=True)

    def _upload_url(self, stylesheet) -> Optional[str]:  # noqa
        if stylesheet.id is None:
            return None
        return url_for("api.v1.stylesheet.upload", stylesheet_id=stylesheet.id)
