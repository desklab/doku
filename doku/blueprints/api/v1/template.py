from flask import Blueprint, jsonify
from sqlalchemy import and_
from werkzeug.exceptions import BadRequest

from doku import db
from doku.blueprints.api.v1.base import api_view_factory, BaseApiView
from doku.models.schemas import TemplateSchema
from doku.models.template import Template, Stylesheet, template_stylesheet_relation
from doku.utils.db import get_or_404
from doku.utils.decorators import login_required

bp = Blueprint("template", __name__)


TemplateApiView = api_view_factory(
    Template, TemplateSchema,
    register=True, register_args=(bp, "api", "/")
)


@bp.route("/<int:template_id>/stylesheet", methods=["POST"])
def add_stylesheet(template_id: int):
    template: Template = get_or_404(
        db.session.query(Template).filter_by(id=template_id)
    )
    template_schema = TemplateSchema(include=("styles",))
    data = BaseApiView.all_request_data()
    if isinstance(data, list):
        for entry in data:
            style: Stylesheet = get_or_404(
                db.session.query(Stylesheet).filter_by(**entry)
            )
            template.styles.append(style)
    else:
        style: Stylesheet = get_or_404(db.session.query(Stylesheet).filter_by(**data))
        template.styles.append(style)
    db.session.commit()
    return jsonify(template_schema.dump(template))


@bp.route("/<int:template_id>/stylesheet", methods=["DELETE"])
def remove_stylesheet(template_id: int):
    template: Template = get_or_404(
        db.session.query(Template).filter_by(id=template_id)
    )
    data = BaseApiView.all_request_data()
    if isinstance(data, list):
        for entry in data:
            if not hasattr(entry, "id"):
                raise BadRequest("Required property: id")
            delete_relation = template_stylesheet_relation.delete().where(
                and_(
                    template_stylesheet_relation.c.template_id == template.id,
                    template_stylesheet_relation.c.style_id == entry.get("id"),
                )
            )
            db.session.execute(delete_relation)
    elif isinstance(data, dict):
        delete_relation = template_stylesheet_relation.delete().where(
            and_(
                template_stylesheet_relation.c.template_id == template.id,
                template_stylesheet_relation.c.style_id == data.get("id"),
            )
        )
        db.session.execute(delete_relation)
    db.session.commit()
    template_schema = TemplateSchema(
        include=("styles",), instance=template, session=db.session
    )
    return jsonify(template_schema.dump(template))
