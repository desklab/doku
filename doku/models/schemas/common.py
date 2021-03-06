from typing import Optional, Union

from flask import request, jsonify, url_for, has_request_context
from marshmallow import EXCLUDE, RAISE, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from werkzeug.exceptions import BadRequest

from doku import db
from doku.utils import EMPTY
from doku.utils.db import get_or_404, get_pagination_page, get_ordering


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
            if request.json is not None:
                if "includes" in request.json:
                    extra_includes |= set(request.json.get("includes"))
                if "excludes" in request.json:
                    extra_excludes |= set(request.json.get("excludes"))
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
            db.session.query(cls.Meta.model).filter_by(id=instance_id)  # noqa
        )
        schema = cls(many=False, include_request=True)
        return jsonify(schema.dump(instance))

    @classmethod
    def get_all(cls):
        # Get page page and ordering. If no specific order and direction
        # has been specified, None will be returned. ``order_by`` will
        # not complain about None being passed, so no worries there.
        page = get_pagination_page()
        ordering, order, direction = get_ordering(
            cls.Meta.model, default_order=None, default_dir=None
        )
        # Create a copy of request arguments and drop all entries that
        # are pagination specific
        data = dict(request.args.copy())
        data.pop("page", None)
        data.pop("order", None)
        data.pop("dir", None)
        schemas = cls(many=True, include_request=True)
        pagination = (
            cls.Meta.model.query.filter_by(**data)
            .order_by(ordering)
            .paginate(page=page, per_page=10)  # noqa
        )
        result = schemas.dump(pagination.items)
        response = {
            "meta": {
                "pages": [page for page in pagination.iter_pages()],
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
                "next_num": pagination.next_num,
                "prev_num": pagination.prev_num,
                "page_count": pagination.pages,
                "per_page": pagination.per_page,
            },
            "result": result,
        }
        return jsonify(response)

    @classmethod
    def update(cls, commit=True):
        data = cls.all_request_data()
        schema = cls(
            unknown=EXCLUDE,
            partial=True,
            session=db.session,
            many=isinstance(data, list),
            include_request=True,
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
            unknown=RAISE,
            session=db.session,
            partial=True,
            many=isinstance(data, list),
            include_request=True,
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
            db.session.query(cls.Meta.model).filter_by(id=instance_id)  # noqa
        )
        db.session.delete(instance)
        if commit:
            db.session.commit()
        return jsonify({"success": True})
