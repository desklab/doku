from typing import Optional

from flask import url_for
from marshmallow import fields
from marshmallow_sqlalchemy import auto_field, SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Nested

from doku.models import DateSchemaMixin
from doku.models.document import Document, Variable


class DocumentSchema(SQLAlchemySchema, DateSchemaMixin):
    class Meta:
        model = Document
        load_instance = True

    id = auto_field()
    name = auto_field()
    template = Nested('TemplateSchema', exclude=('documents',))
    variables = Nested('VariableSchema', exclude=('document',), many=True)
    public_url = fields.Method(
        'get_public_url', dump_only=True, allow_none=True
    )
    render_url = fields.Method(
        'get_render_url', dump_only=True, allow_none=True
    )
    update_url = fields.Method(
        'get_update_url', dump_only=True, allow_none=True
    )

    def get_update_url(self, document) -> Optional[str]:
        if document.id is None:
            return None
        return url_for('api.v1.document.update', document_id=document.id)

    def get_public_url(self, document) -> Optional[str]:
        if document.id is None:
            return None
        return url_for('document.index', document_id=document.id)

    def get_render_url(self, document) -> Optional[str]:
        if document.id is None:
            return None
        return url_for('document.render', document_id=document.id)


class VariableSchema(SQLAlchemySchema, DateSchemaMixin):
    class Meta:
        model = Variable
        load_instance = True

    id = auto_field()
    name = auto_field()
    content = auto_field()
    compiled_content = auto_field(dump_only=True)
    document_id = auto_field(load_only=True)
    parent_id = auto_field(load_only=True)
    parent = Nested('VariableSchema', allow_none=True, exclude=('children',))
    document = Nested('DocumentSchema', exclude=('variables',))
    children = Nested('VariableSchema', many=True)
    used = fields.Boolean(dump_only=True)
    is_list = fields.Boolean(dump_only=True)

    api_url = fields.Method(
        'get_api_url', dump_only=True, allow_none=True
    )
    delete_url = fields.Method(
        'get_delete_url', dump_only=True, allow_none=True
    )
    create_url = fields.Method(
        'get_create_url', dump_only=True, allow_none=True
    )

    def get_api_url(self, variable) -> Optional[str]:
        if variable.id is None:
            return None
        return url_for('api.v1.variable.update', variable_id=variable.id)

    def get_delete_url(self, variable) -> Optional[str]:
        if variable.id is None:
            return None
        return url_for('api.v1.variable.delete', variable_id=variable.id)

    def get_create_url(self, variable) -> Optional[str]:
        if variable.id is None:
            return None
        return url_for('api.v1.variable.create')
