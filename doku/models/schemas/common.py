from typing import Optional

from flask import request, jsonify, url_for, has_request_context
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from doku.models import db
from doku.utils import EMPTY
from doku.utils.db import get_or_404


class NotEmptyString(fields.String):
    def __init__(self, *args, allow_none=False, **kwargs):
        super(NotEmptyString, self).__init__(*args, allow_none=allow_none, **kwargs)

    def _deserialize(self, value, *args, **kwargs):
        if value == "" or value in EMPTY:
            value = None
        return super(NotEmptyString, self)._deserialize(value, *args, **kwargs)


class DokuSchema(SQLAlchemySchema):
    def __init__(self, *args, include_request=False, **kwargs):
        include = set(kwargs.pop("include", {}))
        if has_request_context() and include_request:
            extra_includes = set(request.args.getlist("includes[]", type=str))
            extra_excludes = set(request.args.getlist("excludes[]", type=str))
            if request.get_json(silent=True) is not None:
                if "includes" in request.get_json(silent=True):
                    extra_includes |= set(request.get_json(silent=True).get("includes"))
                if "excludes" in request.get_json(silent=True):
                    extra_excludes |= set(request.get_json(silent=True).get("excludes"))
        else:
            extra_includes = extra_excludes = set()
        super(DokuSchema, self).__init__(*args, **kwargs)
        if len(include) + len(extra_includes) + len(extra_excludes) != 0:
            self.exclude: set = self.exclude - include
            self.exclude: set = self.exclude - extra_includes
            self.exclude: set = self.exclude | extra_excludes
            self._init_fields()

    # This is used to automatically ignore the csrf token that might be
    # submitted when using forms.
    _csrf_token = fields.String(required=False, load_only=True, data_key="csrf_token")


class ApiSchema(DokuSchema):
    API_PREFIX = "api.v1"
    GET_VIEW_SUFFIX = "api"
    GET_ALL_VIEW_SUFFIX = "api"
    UPDATE_VIEW_SUFFIX = "api"
    CREATE_VIEW_SUFFIX = "api"
    DELETE_VIEW_SUFFIX = "api"

    get_url = fields.Method("_get_url", dump_only=True, allow_none=True)
    get_all_url = fields.Method("_get_all_url", dump_only=True, allow_none=True)
    update_url = fields.Method("_update_url", dump_only=True, allow_none=True)
    delete_url = fields.Method("_delete_url", dump_only=True, allow_none=True)
    create_url = fields.Method("_create_url", dump_only=True, allow_none=True)

    @staticmethod
    @property
    def API_NAME():  # noqa
        """Abstract property used as a placeholder for implementation"""
        raise NotImplementedError("API_NAME must be implemented")

    def _get_url(self, instance) -> Optional[str]:
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.GET_VIEW_SUFFIX}"
        if instance.id is None:
            return None
        return url_for(view, **{f"{self.API_NAME}_id": instance.id})

    def _get_all_url(self, instance) -> str:  # noqa
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.GET_ALL_VIEW_SUFFIX}"
        return url_for(view)

    def _update_url(self, instance) -> str:  # noqa
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.UPDATE_VIEW_SUFFIX}"
        return url_for(view)

    def _delete_url(self, instance) -> Optional[str]:
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.DELETE_VIEW_SUFFIX}"
        if instance.id is None:
            return None
        return url_for(view, **{f"{self.API_NAME}_id": instance.id})

    def _create_url(self, instance) -> str:  # noqa
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.CREATE_VIEW_SUFFIX}"
        return url_for(view)
