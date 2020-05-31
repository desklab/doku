from typing import Optional

from flask import jsonify, url_for
from marshmallow import fields, RAISE, ValidationError, EXCLUDE
from marshmallow_sqlalchemy import auto_field, SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Nested
from werkzeug.exceptions import BadRequest

from doku.models import DateSchemaMixin, db
from doku.models.document import Document, Variable
from doku.models.schemas.common import ApiSchemaMixin, DokuSchema
from doku.models.template import Template, DEFAULT_TEMPLATE, Stylesheet
from doku.utils.db import get_or_create


class DocumentSchema(DokuSchema, DateSchemaMixin, ApiSchemaMixin):
    class Meta:
        model = Document
        exclude = ("template", "variables")
        load_instance = True

    API_NAME = "document"

    id = auto_field()
    name = auto_field()
    public = auto_field()
    template_id = auto_field(load_only=True)
    template = Nested("TemplateSchema", exclude=("documents",))
    variables = Nested("VariableSchema", exclude=("document",), many=True, partial=True)
    render_url = fields.Method("_render_url", dump_only=True, allow_none=True)
    public_url = fields.Method("_public_url", dump_only=True, allow_none=True)

    def _render_url(self, instance) -> Optional[str]:
        if instance.id is None:
            return None
        return url_for("document.render", document_id=instance.id)

    def _public_url(self, instance) -> Optional[str]:
        if instance.id is None:
            return None
        return url_for("document.index", document_id=instance.id)

    @classmethod
    def create(cls, commit=True):
        data = cls.all_request_data()
        schema = cls(
            unknown=RAISE, session=db.session, partial=True, many=isinstance(data, list)
        )
        try:
            document = schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), BadRequest.code
        if document.template_id is None:
            template = Template(name=f"{document.name} - Template")
            template.source = DEFAULT_TEMPLATE
            stylesheet = Stylesheet(name=f"{document.name} - Styles")
            template.base_style = stylesheet
            document.template = template
            db.session.add(stylesheet)
            db.session.add(template)
        else:
            document.template = (
                db.session.query(Template).filter_by(id=document.template_id).one()
            )
        for name in document.template.available_fields:
            variable = Variable(document=document, name=name)
            db.session.add(variable)
        db.session.add(document)
        if commit:
            db.session.commit()
        result = schema.dump(document)
        return jsonify(result)

    @classmethod
    def update(cls, commit=True):
        data = cls.all_request_data()
        schema = cls(
            unknown=EXCLUDE,
            partial=True,
            session=db.session,
            many=isinstance(data, list),
        )
        try:
            document = schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), BadRequest.code
        for name in document.template.available_fields:
            get_or_create(Variable, document=document, name=name)
        if commit:
            db.session.commit()
        result = schema.dump(document)
        return jsonify(result)


class VariableSchema(DokuSchema, DateSchemaMixin, ApiSchemaMixin):
    class Meta:
        model = Variable
        load_instance = True

    API_NAME = "variable"

    id = auto_field()
    name = auto_field()
    use_markdown = auto_field()
    css_class = auto_field()
    content = auto_field()
    compiled_content = auto_field(dump_only=True)
    document_id = auto_field(load_only=True)
    parent_id = auto_field(load_only=True)
    parent = Nested("VariableSchema", allow_none=True, exclude=("children",))
    document = Nested("DocumentSchema", exclude=("variables",), dump_only=True)
    children = Nested("VariableSchema", exclude=("document",), many=True, partial=True)
    used = fields.Boolean(dump_only=True)
    is_list = fields.Boolean(dump_only=True)
