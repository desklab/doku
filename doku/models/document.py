from typing import Optional, List

import markdown
from sqlalchemy.orm import Session
from sqlalchemy import event

from doku.models import db, DateMixin


class Document(db.Model, DateMixin):
    """Document Model
    """

    __tablename__ = 'doku_document'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    public = db.Column(db.Boolean)
    template_id = db.Column(
        db.Integer,
        db.ForeignKey('doku_template.id'),
        nullable=True
    )

    template = db.relationship('Template', back_populates='documents')
    variables = db.relationship('Variable', back_populates='document')

    def __str__(self):
        return self.name

    @property
    def html(self):
        return self.template.source

    @property
    def filename(self):
        return '_'.join(self.name.split()).lower()

    def render(self):
        return self.template.render(self.variables)


def compile_content(context) -> Optional[str]:
    if 'content' not in context.current_parameters:
        raise ValueError('content not in current_parameters')
    content = context.current_parameters['content']
    if content is None:
        return ''
    return markdown.markdown(content, extensions=['codehilite'])


class Variable(db.Model, DateMixin):
    """Variable

    Used to store the actual markdown content of a document.

    As we work with Jinja2 templates for out :class:`Template` class,
    they are basically passed as a context.
    """
    __tablename__ = 'doku_variable'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    content = db.Column(db.UnicodeText, nullable=False, default='', )
    compiled_content = db.Column(
        db.UnicodeText,
        nullable=False,
        default=''
    )
    document_id = db.Column(
        db.Integer,
        db.ForeignKey('doku_document.id'),
        nullable=False
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('doku_variable.id'),
        nullable=True
    )

    children = db.relationship(
        'Variable',
        backref=db.backref('parent', remote_side=[id])
    )
    document = db.relationship('Document', back_populates='variables')

    @property
    def used(self) -> bool:
        return self.name in self.document.template.available_fields

    @property
    def is_list(self) -> bool:
        return self.name.endswith('_list')

    @property
    def as_list(self) -> List[str]:
        if not self.is_list:
            raise ValueError(f'{self.name} is not a list')
        return [var.compiled_content for var in self.children]


@event.listens_for(Variable, 'before_update')
@event.listens_for(Variable, 'before_insert')
def before_any_compiler(mapper, connection, target):
    content = target.content
    if content is None or content is '':
        target.content = ''
        target.compiled_content = ''
        return
    else:
        target.compiled_content = markdown.markdown(content, extensions=['codehilite'])
