from flask import session

from doku.models import db, DateMixin


class Document(db.Model, DateMixin):
    """Document Model"""

    __tablename__ = "doku_document"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    public = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey("doku_user.id"), nullable=False)
    template_id = db.Column(
        db.Integer, db.ForeignKey("doku_template.id"), nullable=False
    )

    template = db.relationship("Template", back_populates="documents")
    author = db.relationship("User")

    # All variables
    variables = db.relationship(
        "Variable", cascade="all,delete", back_populates="document"
    )
    variable_groups = db.relationship(
        "VariableGroup", back_populates="document", cascade="all,delete"
    )
    # Root variables are variables that do not belong to any variable
    # group
    root_variables = db.relationship(
        "Variable",
        primaryjoin="and_(Variable.document_id == Document.id, Variable.group_id == null())",
    )

    def __init__(self, *args, author_id=None, author=None, **kwargs):
        if author_id is None and author is None:
            author_id = session.get("id", None)
            self.author_id = author_id
            super(Document, self).__init__(*args, **kwargs)
        else:
            super(Document, self).__init__(
                *args, author_id=author_id, author=author, **kwargs
            )

    def __str__(self):
        return self.name

    @property
    def html(self):
        return self.template.source

    @property
    def filename(self):
        return "_".join(self.name.split()).lower()

    def render(self):
        return self.template.render(self.variables)

    def write_pdf(self, path):
        return self.template.write_pdf(self.variables, path)
