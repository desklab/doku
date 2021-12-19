from flask import Blueprint

from doku.blueprints.api.v1.base import api_view_factory
from doku.models.schemas import VariableSchema
from doku.models.variable import Variable

bp = Blueprint("variable", __name__)


TemplateApiView = api_view_factory(
    Variable, VariableSchema,
    register=True, register_args=(bp, "api", "/")
)
