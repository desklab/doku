import typing as t
import warnings

from flask import jsonify, request
from flask.scaffold import Scaffold
from flask.views import MethodView
from marshmallow import RAISE, ValidationError, EXCLUDE
from werkzeug.exceptions import BadRequest

from doku.models import db
from doku.models.schemas.common import ApiSchema
from doku.signals import model_created, model_updated
from doku.utils.db import get_or_404, get_pagination_page, get_ordering


class BaseApiView(MethodView):
    model: t.Type[db.Model]
    schema: t.Type[ApiSchema]
    pk_field: str = "pk"
    pk_type: str = "int"

    def get_instance(self, pk: pk_type) -> "model":
        return get_or_404(db.session.query(self.model).filter_by(id=pk))

    def get(self, pk: t.Optional[pk_type]):
        if pk is None:
            return self.get_all()
        else:
            instance = self.get_instance(pk)
            schema = self.schema(many=False, include_request=True)
            return jsonify(schema.dump(instance))

    def get_all(self):
        # Get page and ordering. If no specific order and direction
        # has been specified, None will be returned. ``order_by`` will
        # not complain about None being passed, so no worries there.
        page = get_pagination_page()
        ordering, order, direction = get_ordering(
            self.model, default_order=None, default_dir=None
        )
        # Create a copy of request arguments and drop all entries that
        # are pagination specific
        data = dict(request.args.copy())
        data.pop("page", None)
        data.pop("order", None)
        data.pop("dir", None)
        schemas = self.schema(many=True, include_request=True)
        pagination = (
            self.model.query.filter_by(**data)
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

    def post(self, *, commit: bool = True):
        data = self.all_request_data()
        schema = self.schema(
            session=db.session,
            partial=True,
            many=isinstance(data, list),
            include_request=True,
            unknown=RAISE,
        )
        try:
            instance = schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), BadRequest.code
        db.session.add(instance)
        model_created.send(self.model, instance=instance)
        if commit:
            db.session.commit()
        result = schema.dump(instance)
        return jsonify(result), 200

    def put(self, pk: t.Optional[pk_type], *, commit: bool = True):
        return self.update(pk=pk, commit=commit)

    def patch(self, pk: t.Optional[pk_type], *, commit: bool = True):
        return self.update(pk=pk, commit=commit)

    def delete(self, pk: pk_type, commit: bool = True):
        instance = self.get_instance(pk)
        db.session.delete(instance)
        if commit:
            db.session.commit()
        return jsonify({"success": True})

    def update(self, *, pk: t.Optional[pk_type] = None, commit: bool = True):
        data = self.all_request_data()
        if pk is not None:
            instance = self.get_instance(pk)
            schema = self.schema(
                instance=instance,
                session=db.session,
                unknown=EXCLUDE,
                include_request=True,
                many=False,
            )
        else:
            schema = self.schema(
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

        # Send signals that instance will be updated
        if isinstance(instance, list):
            for _instance in instance:
                model_updated.send(self.model, instance=_instance)
        else:
            model_updated.send(self.model, instance=instance)

        if commit:
            db.session.commit()
        result = schema.dump(instance)
        return jsonify(result)

    @staticmethod
    def all_request_data(include_args=False) -> t.Union[dict, list]:
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
    def register(cls, app: Scaffold, name: str, url: str):
        if not url.endswith("/"):
            warnings.warn(
                f"URL '{url}' does not end with a trailing slash ('/').", UserWarning
            )
            url = f"{url}/"
        view = cls.as_view(name)
        # Get all entries
        app.add_url_rule(url, defaults=dict(pk=None), view_func=view, methods=["GET"])
        # Create entry
        app.add_url_rule(url, view_func=view, methods=["POST"])
        # Methods on existing entries
        app.add_url_rule(
            f"{url}<{cls.pk_type}:{cls.pk_field}>/",
            view_func=view,
            methods=["GET", "PUT", "PATCH", "DELETE"]
        )
        # Bulk operations
        app.add_url_rule(
            url,
            defaults=dict(pk=None),
            view_func=view,
            methods=["PUT", "PATCH"]
        )


def api_view_factory(
    view_model: t.Type[db.Model],
    view_schema: t.Type[ApiSchema],
    view_pk_field: str = BaseApiView.pk_field,
    view_pk_type: str = BaseApiView.pk_type,
    register: bool = False,
    register_args: t.Optional[tuple] = None,
) -> t.Type[BaseApiView]:
    class ApiView(BaseApiView):
        model: t.Type[db.Model] = view_model
        schema: t.Type[ApiSchema] = view_schema
        pk_field: str = view_pk_field
        pk_type: str = view_pk_type

    if register:
        if not register_args:
            raise ValueError("'register_args' is required for registering the API view")
        ApiView.register(*register_args)

    return ApiView
