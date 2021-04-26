from typing import Optional

from flask import jsonify, url_for
from marshmallow import fields, RAISE, ValidationError, EXCLUDE
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from werkzeug.exceptions import BadRequest

from doku.models import DateSchemaMixin, db
from doku.models.document import Document
from doku.models.schemas.common import ApiSchema, NotEmptyString
from doku.models.template import Template, DEFAULT_TEMPLATE
from doku.models.variable import Variable
from doku.utils.db import get_or_create


class DocumentSchema(ApiSchema, DateSchemaMixin):
    class Meta:
        model = Document
        exclude = ("template", "variables", "variable_groups", "root_variables")
        load_instance = True

    API_NAME = "document"

    id = auto_field()
    name = NotEmptyString()
    public = auto_field()
    template_id = auto_field(load_only=True)

    template = Nested("TemplateSchema", exclude=("documents",))
    variables = Nested(
        "VariableSchema", exclude=("document",), many=True, metadata=dict(partial=True)
    )
    variable_groups = Nested("VariableGroupSchema", exclude=("document",), many=True)
    root_variables = Nested(
        "VariableSchema", exclude=("document",), many=True, metadata=dict(partial=True)
    )

    render_url = fields.Method("_render_url", dump_only=True, allow_none=True)
    public_url = fields.Method("_public_url", dump_only=True, allow_none=True)

    def _render_url(self, instance) -> Optional[str]:  # noqa
        if instance.id is None:
            return None
        return url_for("document.render", document_id=instance.id)

    def _public_url(self, instance) -> Optional[str]:  # noqa
        if instance.id is None:
            return None
        return url_for("document.index", document_id=instance.id)

    @classmethod
    def create(cls, commit=True):
        data = cls.all_request_data()
        schema = cls(
            unknown=RAISE,
            session=db.session,
            metadata=dict(partial=True),
            many=isinstance(data, list),
            include_request=True,
        )
        try:
            document = schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), BadRequest.code
        if document.template_id is None:
            template = Template(name=f"Template for {document.name}")
            template.source = DEFAULT_TEMPLATE
            document.template = template
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
            metadata=dict(partial=True),
            session=db.session,
            many=isinstance(data, list),
            include_request=True,
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
