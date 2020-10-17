from flask import Blueprint, render_template

from doku import db
from doku.models.schemas import TemplateSchema, StylesheetSchema
from doku.models.template import Template
from doku.utils.db import get_or_404, get_pagination_page
from doku.utils.decorators import login_required

bp = Blueprint("template", __name__)

@bp.route("/", methods=["GET"])
@login_required
def index_all():
    page = get_pagination_page()
    templates = (
        db.session.query(Template).paginate(page=page, per_page=10)
    )
    template_schema = TemplateSchema(session=db.session, many=True)
    return render_template(
        "sites/templates.html",
        templates_json=template_schema.dumps(templates.items),
        templates=templates
    )

@bp.route("/<int:template_id>", methods=["GET"])
@login_required
def index(template_id: int):
    template: Template = get_or_404(
        db.session.query(Template).filter_by(id=template_id)
    )
    template_schema = TemplateSchema(session=db.session)
    stylesheet_schemas = StylesheetSchema(session=db.session, many=True)
    return render_template(
        "sites/edit_template.html",
        template_json=template_schema.dumps(template),
        stylesheets_json=stylesheet_schemas.dumps(template.styles),
    )
