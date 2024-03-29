import functools
from typing import List, Tuple

from jinja2 import Environment, meta
from jinja2 import Template as Jinja2Template
from pygments.formatters.html import HtmlFormatter
from sqlalchemy import Index
from weasyprint import HTML, CSS

from doku.models import db, DateMixin, TSVector
from doku.utils.weasyfetch import url_fetcher

DEFAULT_TEMPLATE = """<!doctype html>
<html lang="de">
<head>
  <title>{{ Document_Title }}</title>
  <meta charset="utf-8">
</head>
<body>

</body>
</html>"""

template_stylesheet_relation = db.Table(
    "doku_template_stylesheet_relation",
    db.Model.metadata,
    db.Column("template_id", db.Integer, db.ForeignKey("doku_template.id")),
    db.Column("style_id", db.Integer, db.ForeignKey("doku_stylesheet.id")),
)


class Template(db.Model, DateMixin):
    """Template Model

    Used to store Jinja2 templates that can be populated with various
    variables.
    Styles are implemented using relations to the :class:`Stylesheet`
    model. For each template there is a :attr:`base_style`, which
    corresponds to a global stylesheet for multi-document presets.
    """

    __tablename__ = "doku_template"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    source = db.Column(db.UnicodeText, nullable=True, default=DEFAULT_TEMPLATE)

    documents = db.relationship("Document", back_populates="template")
    styles = db.relationship(
        "Stylesheet", secondary=template_stylesheet_relation, back_populates="templates"
    )

    __ts_vector__ = db.Column(
        TSVector(),
        db.Computed(
            "to_tsvector('english', name)",
            persisted=True
        )
    )

    __table_args__ = (
        Index('doku_template___ts_vector__', __ts_vector__, postgresql_using='gin'),
    )

    def __str__(self):
        return self.name

    @property
    @functools.lru_cache(maxsize=512)
    def available_fields(self):
        env = Environment()
        content = env.parse(self.source)
        return meta.find_undeclared_variables(content)

    def render(self, variables) -> bytes:
        html, stylesheets = self._render(variables)
        return html.write_pdf(stylesheets=stylesheets)

    def html(self, variables) -> HTML:
        html, _ = self._render(variables)
        return html

    def _render(self, variables) -> Tuple[HTML, List[CSS]]:
        stylesheets = [
            style.as_css for style in self.styles if style.source is not None
        ]
        template = Jinja2Template(self.source)
        context: dict = {
            var.name: var.get_compiled_content()
            for var in variables
            if not var.is_list or var.parent_id is not None
        }
        context.update({var.name: var.as_list for var in variables if var.is_list})
        source = template.render(**context)
        if "codehilite" in source:
            stylesheets.append(CSS(string=HtmlFormatter().get_style_defs()))
        return HTML(string=source, base_url=".", url_fetcher=url_fetcher), stylesheets

    def write_pdf(self, variables, path):
        html, stylesheets = self._render(variables)
        return html.write_pdf(target=path, stylesheets=stylesheets)


class Stylesheet(db.Model, DateMixin):
    """Stylesheet Model

    This model is used in conjunction with the :class:`Template` model.
    While the Template model provides the Jinja2 (HTML) template, this
    model will serve the stylesheet. Separating both types will help us
    achieve a more modular templating engine with base styles and custom
    styles that can be changed globally.
    """

    __tablename__ = "doku_stylesheet"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    source = db.Column(db.UnicodeText, nullable=True)

    templates = db.relationship(
        "Template", secondary=template_stylesheet_relation, back_populates="styles"
    )

    MAX_CONTENT_LENGTH = 125000

    __ts_vector__ = db.Column(
        TSVector(),
        db.Computed(
            "to_tsvector('english', name)",
            persisted=True
        )
    )

    __table_args__ = (
        Index('doku_stylesheet___ts_vector__', __ts_vector__, postgresql_using='gin'),
    )

    def __str__(self):
        return self.name

    @property
    def as_css(self) -> CSS:
        return CSS(string=self.source)
