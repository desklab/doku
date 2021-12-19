from flask import Blueprint

from doku.blueprints.api.v1.base import api_view_factory
from doku.models.schemas import VariableGroupSchema
from doku.models.variable import VariableGroup

bp = Blueprint("vargroup", __name__)


TemplateApiView = api_view_factory(
    VariableGroup, VariableGroupSchema,
    register=True, register_args=(bp, "api", "/")
)
