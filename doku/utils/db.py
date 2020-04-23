from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound

from doku import db


def get_or_404(query: Query, query_type: str = 'one'):
    """

    .. todo :: use flask-sqlalchemy's get_or_404 instead

    :param query: The queryset that should be queried. E.g.
        ``session.db.query(Model).filter(something=='Foo')``
    :param query_type: String identifier for method. Either ``one`` or ``all``
    """
    try:
        if query_type == 'one':
            return query.one()
        elif query_type == 'all':
            return query.all()
        else:
            raise ValueError(f'Unexpected type {query_type}. Allowed types: one, all')
    except NoResultFound:
        raise NotFound()


def get_or_create(model: db.Model, commit=False, **kwargs) -> db.Model:
    """Get or create

    """
    try:
        return db.session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        instance = model(**kwargs)
        db.session.add(instance)
        if commit:
            db.session.commit()
        return instance
