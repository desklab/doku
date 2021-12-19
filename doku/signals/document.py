import typing as t

from doku.models import db
from doku.models.base import (
    Document,
    Template,
    Variable
)
from doku.signals import model_created, model_updated
from doku.utils.db import get_or_create, create_if_not_exists


@model_created.connect_via(Document)
def create_missing_vars(sender: t.Type[db.Model], instance: Document, **extra):
    template: Template = instance.template
    for name in template.available_fields:
        variable = Variable(document=instance, name=name)
        db.session.add(variable)


@model_updated.connect_via(Document)
def update_missing_vars(sender: t.Type[Document], instance: Document, **extra):
    template: Template = instance.template
    for name in template.available_fields:
        create_if_not_exists(Variable, document=instance, name=name)


@model_updated.connect_via(Template)
def update_missing_vars_for_template(
    sender: t.Type[Template],
    instance: Template,
    **extra
):
    documents: t.List[Document] = instance.documents
    available_fields: tuple = instance.available_fields
    for document in documents:
        for name in available_fields:
            create_if_not_exists(Variable, document=document, name=name)
