from typing import Optional

from sqlalchemy.orm import Query, Session
from sqlalchemy.types import String
from sqlalchemy import inspect, desc, asc, func
from sqlalchemy.orm.exc import NoResultFound
from flask_sqlalchemy.model import DeclarativeMeta
from werkzeug.exceptions import NotFound
from flask import request

from doku import db


def get_or_404(query: Query, query_type: str = "one"):
    """

    .. todo :: use flask-sqlalchemy's get_or_404 instead

    :param query: The queryset that should be queried. E.g.
        ``session.db.query(Model).filter(something=='Foo')``
    :param query_type: String identifier for method. Either ``one`` or ``all``
    """
    try:
        if query_type == "one":
            return query.one()
        elif query_type == "all":
            return query.all()
        else:
            raise ValueError(f"Unexpected type {query_type}. Allowed types: one, all")
    except NoResultFound:
        raise NotFound()


def get_or_create(model: db.Model, commit=False, **kwargs) -> db.Model:
    """Get or create"""
    try:
        return db.session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        instance = model(**kwargs)
        db.session.add(instance)
        if commit:
            db.session.commit()
        return instance


def get_pagination_page() -> Optional[int]:
    page = request.args.get("page", None)
    if page is not None:
        try:
            page = int(page)
        except ValueError:
            return None
    return page


def get_ordering(
    model: type(DeclarativeMeta), default_order: str = None, default_dir: str = None
) -> Optional[tuple]:
    """Get Ordering

    Get ordering from request arguments

    :param model: The model that should be ordered
    :param default_order: The default order if no order is selected
    :param default_dir: The default direction if no direction is
        specified. Can be either "asc" or "desc"
    :returns: The ordering object, the order string and direction string
    """
    if not isinstance(model, DeclarativeMeta):
        raise ValueError(f"Expected type DeclarativeMeta but got {type(model)}")
    order = request.args.get("order", default_order)
    if order is None:
        return None, None, None
    if order in inspect(model).column_attrs.keys():
        ordering = getattr(model, order)
        if isinstance(ordering.type, String):
            ordering = func.lower(ordering)
    else:
        return None, None, None
    dir_arg = request.args.get("dir", default_dir)
    if dir_arg not in ["asc", "desc"]:
        dir_arg = default_dir
    if dir_arg == "asc":
        ordering = asc(ordering)
    elif dir_arg == "desc":
        ordering = desc(ordering)
    return ordering, order, dir_arg
