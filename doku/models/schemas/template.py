from typing import Optional

from flask import url_for
from marshmallow import fields
from marshmallow_sqlalchemy import auto_field, SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Nested

from doku.models import DateSchemaMixin
from doku.models.template import Template, Stylesheet


class TemplateSchema(SQLAlchemySchema, DateSchemaMixin):
    class Meta:
        model = Template
        load_instance = True

    id = auto_field()
    name = auto_field()
    source = auto_field()
    documents = Nested('DocumentSchema', many=True, exclude=('template',))
    base_style = Nested('StylesheetSchema', exclude=('base_templates',))
    styles = Nested('StylesheetSchema', many=True, exclude=('templates',))
    available_fields = fields.List(fields.String, dump_only=True)

    update_url = fields.Method(
        'get_update_url', dump_only=True, allow_none=True
    )

    def get_update_url(self, template) -> Optional[str]:
        if template.id is None:
            return None
        return url_for('api.v1.template.update', template_id=template.id)


class StylesheetSchema(SQLAlchemySchema, DateSchemaMixin):
    class Meta:
        model = Stylesheet
        load_instance = True

    id = auto_field()
    name = auto_field()
    source = auto_field()
    base_templates = Nested('TemplateSchema', exclude=('base_style',), many=True)
    templates = Nested('TemplateSchema', exclude=('styles',), many=True)

    update_url = fields.Method(
        'get_update_url', dump_only=True, allow_none=True
    )

    def get_update_url(self, stylesheet) -> Optional[str]:
        if stylesheet.id is None:
            return None
        return url_for('api.v1.stylesheet.update', stylesheet_id=stylesheet.id)
