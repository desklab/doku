from sqlalchemy import event

from doku.models import db, DateMixin
from doku.utils.markdown import compile_content


class Snippet(db.Model, DateMixin):
    """Snippet Model

    Snippets are reusable pieces of text (e.g. markdown) that can
    be used across documents.
    """

    __tablename__ = "doku_snippet"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)

    use_markdown = db.Column(db.Boolean, default=True)
    css_class = db.Column(db.String(255), unique=False, nullable=True, default="")
    content = db.Column(db.UnicodeText, nullable=False, default="")
    compiled_content = db.Column(db.UnicodeText, nullable=False, default="")

    used_by = db.relationship("Variable")

    def __str__(self):
        return f"Snippet {self.name}"


@event.listens_for(Snippet.use_markdown, "set")
def before_content_compiler(target, value, old_value, initiator):  # noqa
    target.compiled_content = compile_content(target.content, target.css_class, value)


@event.listens_for(Snippet.css_class, "set")
def before_content_compiler(target, value, old_value, initiator):  # noqa
    target.compiled_content = compile_content(
        target.content, value, target.use_markdown
    )


@event.listens_for(Snippet.content, "set")
def before_content_compiler(target, value, old_value, initiator):  # noqa
    target.compiled_content = compile_content(
        value, target.css_class, target.use_markdown
    )
