import typing as t

from doku.models import db
from doku.models.base import (
    Document,
    Template,
    Variable
)
from doku.models.template import DEFAULT_TEMPLATE
from doku.signals import model_created, model_updated
from doku.utils.db import get_or_create, create_if_not_exists


@model_created.connect_via(Document)
def create_missing_template_vars(sender: t.Type[db.Model], instance: Document, **extra):
    if instance.template_id is None:
        _template = Template(name=f"Template for {instance.name}")
        _template.source = DEFAULT_TEMPLATE
        instance.template = _template
        db.session.add(_template)
    else:
        instance.template = (
            db.session.query(Template).filter_by(id=instance.template_id).one()
        )

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
