from io import BytesIO

from flask import Blueprint, render_template, send_file
from marshmallow import EXCLUDE
from weasyprint import HTML

from doku import db
from doku.models.document import Document
from doku.models.schemas import TemplateSchema, StylesheetSchema
from doku.models.schemas.document import DocumentSchema, VariableSchema
from doku.models.template import Template, Stylesheet
from doku.utils.db import get_or_404
from doku.utils.decorators import login_required


bp = Blueprint('template', __name__)


@bp.route('/<int:template_id>', methods=['GET'])
@login_required
def index(template_id: int):
    template: Template = get_or_404(
        db.session.query(Template).filter_by(id=template_id)
    )
    template_schema = TemplateSchema(session=db.session)
    stylesheet_schemas = StylesheetSchema(session=db.session, many=True)
    return render_template(
        'sites/edit_template.html',
        template_json=template_schema.dumps(template),
        stylesheets_json=stylesheet_schemas.dumps(template.styles)
    )
