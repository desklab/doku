from datetime import datetime, timezone
from typing import Optional, List

from flask_babel import format_timedelta, format_datetime
import markdown
from sqlalchemy.orm import Session
from sqlalchemy import event, asc, update

from doku.models import db, DateMixin
from doku.utils.markdown.extensions import RootClassTreeprocessor, RootClassExtension


class Document(db.Model, DateMixin):
    """Document Model
    """

    __tablename__ = "doku_document"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    public = db.Column(db.Boolean)
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

    children = db.relationship(
        "Variable", cascade="all,delete", backref=db.backref("parent", remote_side=[id])
    )
    document = db.relationship("Document", back_populates="variables")

    @property
    def used(self) -> bool:
        if self.parent_id is not None:
            return True
        return self.name in self.document.template.available_fields

    @property
    def is_list(self) -> bool:
        return self.name.endswith("_list")

    @property
    def as_list(self) -> List[str]:
        if not self.is_list:
            raise ValueError(f"{self.name} is not a list")
        return [var.compiled_content for var in self.children]


@event.listens_for(Variable.content, "set")
@event.listens_for(Variable.use_markdown, "set")
@event.listens_for(Variable.css_class, "set")
def before_any_compiler(target, value, old_value, initiator):
    content = target.content
    if content is None or content is "":
        target.content = ""
        target.compiled_content = ""
        return
    else:
        if target.use_markdown:
            target.compiled_content = markdown.markdown(
                content,
                extensions=[
                    RootClassExtension(root_class=target.css_class),
                    "codehilite",
                    "fenced_code",
                ],
            )
        else:
            target.compiled_content = content


@event.listens_for(Variable, "before_update")
@event.listens_for(Variable, "before_insert")
@event.listens_for(Variable, "before_delete")
def update_parent(mapper, connection, target):
    connection.execute(
        update(Document)
        .where(Document.id == target.document_id)
        .values(last_updated=datetime.now())
    )
