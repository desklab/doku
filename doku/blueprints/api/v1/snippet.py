from flask import Blueprint

from doku.blueprints.api.v1.base import api_view_factory
from doku.models.base import Snippet
from doku.models.schemas import SnippetSchema

bp = Blueprint("snippet", __name__)


SnippetApiView = api_view_factory(
    Snippet, SnippetSchema,
    register=True, register_args=(bp, "api", "/")
)
