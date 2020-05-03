from io import BytesIO

from flask import Blueprint, render_template, send_file
from marshmallow import EXCLUDE
from weasyprint import HTML

from doku import db
from doku.models.document import Document
from doku.models.schemas import TemplateSchema, StylesheetSchema
from doku.models.schemas.document import DocumentSchema, VariableSchema
from doku.utils.db import get_or_404
from doku.utils.decorators import login_required


bp = Blueprint('document', __name__)


@bp.route('/<int:document_id>', methods=['GET'])
@login_required
def index(document_id: int):
    document: Document = get_or_404(
        db.session.query(Document).filter_by(id=document_id)
    )
    doc_schema = DocumentSchema(session=db.session, instance=document)
    var_schemas = VariableSchema(session=db.session, many=True)
    template_schema = TemplateSchema(session=db.session)
    stylesheet_schemas = StylesheetSchema(session=db.session, many=True)
    return render_template(
        'sites/edit.html',
        document_id=document_id,
        document_json=doc_schema.dumps(document),
        variable_json=var_schemas.dumps(document.variables, many=True),
        template_json=template_schema.dumps(document.template),
        stylesheets_json=stylesheet_schemas.dumps(document.template.styles)
    )


@bp.route('/<int:document_id>/render', methods=['GET'])
@login_required
def render(document_id: int):
    document: Document = get_or_404(
        db.session.query(Document).filter_by(id=document_id)
    )
    output = document.render()
    file = BytesIO(output)
    return send_file(
        file,
        mimetype='application/pdf',
        attachment_filename=f'{document.filename}.pdf',
        cache_timeout=0
    )
