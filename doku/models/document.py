from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import event, text, update, func

from doku.models import db, DateMixin
from doku.utils.markdown import compile_content


class Document(db.Model, DateMixin):
    """Document Model
    """

    __tablename__ = "doku_document"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    public = db.Column(db.Boolean)
    author = db.Column(db.Integer, db.ForeignKey("doku_user.id"), nullable=False)
    template_id = db.Column(
        db.Integer, db.ForeignKey("doku_template.id"), nullable=True
    )

    template = db.relationship("Template", back_populates="documents")
    variables = db.relationship(
        "Variable", cascade="all,delete", back_populates="document"
    )

    recent_variable = db.relationship(
        "Variable", order_by="desc(Variable.last_updated)", lazy="dynamic"
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


class Variable(db.Model, DateMixin):
    """Variable

    Used to store the actual markdown content of a document.

    As we work with Jinja2 templates for out :class:`Template` class,
    they are basically passed as a context.
    """

    AUTO_UPDATE = [
        "name",
        "use_markdown",
        "css_class",
        "content",
        "document_id",  # Used for empty children
    ]

    __tablename__ = "doku_variable"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    use_markdown = db.Column(db.Boolean, default=True)
    css_class = db.Column(db.String(255), unique=False, nullable=True, default="")
    content = db.Column(db.UnicodeText, nullable=False, default="")
    compiled_content = db.Column(db.UnicodeText, nullable=False, default="")
    document_id = db.Column(
        db.Integer, db.ForeignKey("doku_document.id"), nullable=False
    )
    parent_id = db.Column(db.Integer, db.ForeignKey("doku_variable.id"), nullable=True)
    snippet_id = db.Column(db.Integer, db.ForeignKey("doku_snippet.id"), nullable=True)

    children = db.relationship(
        "Variable",
        cascade="all,delete",
        backref=db.backref("parent", remote_side=[id]),
        order_by=func.lower(name),
    )
    document = db.relationship("Document", back_populates="variables")
    snippet = db.relationship("Snippet", back_populates="used_by")

    @property
    def used(self) -> bool:
        if self.parent_id is not None:
            return True
        return self.name in self.document.template.available_fields

    @property
    def is_list(self) -> bool:
        return self.name.endswith("_list")

    @property
    def uses_snippet(self) -> bool:
        return self.snippet_id is not None

    @property
    def as_list(self) -> List[str]:
        if not self.is_list:
            raise ValueError(f"{self.name} is not a list")
        return [var.compiled_content for var in self.children]

    def snippet_to_variable(self, commit=True):
        if self.snippet_id is None:
            raise ValueError("Snippet is not provided")
        else:
            self.content = self.snippet.content
            self.compiled_content = self.snippet.compiled_content
            self.use_markdown = self.snippet.use_markdown
            self.css_class = self.snippet.css_class
            self.snippet_id = None

    def __str__(self):
        return f"{self.name} in {self.document.name}"


@event.listens_for(Variable.use_markdown, "set")
def before_content_compiler(target: Variable, value, old_value, initiator):
    target.compiled_content = compile_content(target.content, target.css_class, value)


@event.listens_for(Variable.css_class, "set")
def before_content_compiler(target, value, old_value, initiator):
    target.compiled_content = compile_content(
        target.content, value, target.use_markdown
    )


@event.listens_for(Variable.content, "set")
def before_content_compiler(target, value, old_value, initiator):
    target.compiled_content = compile_content(
        value, target.css_class, target.use_markdown
    )


@event.listens_for(Variable, "before_update")
@event.listens_for(Variable, "before_insert")
@event.listens_for(Variable, "before_delete")
def update_parent(mapper, connection, target):
    connection.execute(
        update(Document)
        .where(Document.id == target.document_id)
        .values(last_updated=datetime.now())
    )
