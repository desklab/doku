from typing import Optional, Union

from flask import request, jsonify, url_for
from marshmallow import EXCLUDE, RAISE, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from werkzeug.exceptions import BadRequest

from doku import db
from doku.utils.db import get_or_404


class DokuSchema(SQLAlchemySchema):
    def __init__(self, *args, **kwargs):
        include = set(kwargs.pop("include", {}))
        super(DokuSchema, self).__init__(*args, **kwargs)
        if len(include) != 0:
            self.exclude: set = self.exclude - include
            self._init_fields()


class ApiSchemaMixin:
    API_PREFIX = "api.v1"
    GET_VIEW_SUFFIX = "get"
    GET_ALL_VIEW_SUFFIX = "get_all"
    UPDATE_VIEW_SUFFIX = "update"
    CREATE_VIEW_SUFFIX = "create"
    DELETE_VIEW_SUFFIX = "delete"

    get_url = fields.Method("_get_url", dump_only=True, allow_none=True)
    get_all_url = fields.Method("_get_all_url", dump_only=True, allow_none=True)
    update_url = fields.Method("_update_url", dump_only=True, allow_none=True)
    delete_url = fields.Method("_delete_url", dump_only=True, allow_none=True)
    create_url = fields.Method("_create_url", dump_only=True, allow_none=True)

    @staticmethod
    @property
    def API_NAME():  # noqa
        """Abstract property used as a placeholder for implementation
        """
        raise NotImplementedError("API_NAME must be implemented")

    def _get_url(self, instance) -> Optional[str]:
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.GET_VIEW_SUFFIX}"
        if instance.id is None:
            return None
        return url_for(view, **{f"{self.API_NAME}_id": instance.id})

    def _get_all_url(self, instance) -> str:
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.GET_ALL_VIEW_SUFFIX}"
        return url_for(view)

    def _update_url(self, instance) -> str:
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.UPDATE_VIEW_SUFFIX}"
        return url_for(view)

    def _delete_url(self, instance) -> Optional[str]:
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.DELETE_VIEW_SUFFIX}"
        if instance.id is None:
            return None
        return url_for(view, **{f"{self.API_NAME}_id": instance.id})

    def _create_url(self, instance) -> str:
        view = f"{self.API_PREFIX}.{self.API_NAME}.{self.CREATE_VIEW_SUFFIX}"
        return url_for(view)

    @staticmethod
    def all_request_data(include_args=False) -> Union[dict, list]:
        """All Request Data

        Get all request data including ``args``, ``form`` and ``json``.

        :param include_args: Whether to include request ``args``. This
            might be handy for get requests. Disabled by default.
        """
        base_data = request.values if include_args else request.form
        data = dict(base_data.copy())
        if request.json is not None:
            if isinstance(request.json, list):
                return request.json
            data.update(request.json)
        return data

    @classmethod
    def get(cls, instance_id: int):
        instance = get_or_404(
            db.session.query(cls.Meta.model).filter_by(id=instance_id)
        )
        schema = cls(many=False)
        return jsonify(schema.dump(instance))

    @classmethod
    def get_all(cls):
        data = request.args
        page = request.args.get("page")
        schemas = cls(many=True)
        instances = (
            cls.Meta.model.query.filter_by(**data)
            .paginate(page=page, per_page=25)
            .items
        )
        result = schemas.dump(instances)
        return jsonify(result)

    @classmethod
    def update(cls, commit=True):
        data = cls.all_request_data()
        schema = cls(
            unknown=EXCLUDE,
            partial=True,
            session=db.session,
            many=isinstance(data, list),
        )
        try:
            instance = schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), BadRequest.code
        if commit:
            db.session.commit()
        result = schema.dump(instance)
        return jsonify(result)

    @classmethod
    def create(cls, commit=True):
        data = cls.all_request_data()
        schema = cls(
            unknown=RAISE, session=db.session, partial=True, many=isinstance(data, list)
        )
        try:
            instance = schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), BadRequest.code
        db.session.add(instance)
        if commit:
            db.session.commit()
        result = schema.dump(instance)
        return jsonify(result)

    @classmethod
    def delete(cls, instance_id: int, commit=True):
        instance = get_or_404(
            db.session.query(cls.Meta.model).filter_by(id=instance_id)
        )
        db.session.delete(instance)
        if commit:
            db.session.commit()
        return jsonify({"success": True})
