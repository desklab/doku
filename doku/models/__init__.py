from datetime import datetime, timezone

from flask_babel import format_timedelta, format_datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import auto_field
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import TSVECTOR

db = SQLAlchemy(session_options={"autoflush": False})


class TSVector(TypeDecorator):
    impl = TSVECTOR


class DateMixin:
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.now)
    last_updated = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )

    @property
    def last_updated_timedelta(self):
        now = datetime.now(tz=timezone.utc)
        last_updated = self.last_updated.astimezone(tz=timezone.utc)
        return format_timedelta(now - last_updated)

    @property
    def last_updated_format(self):
        return format_datetime(self.last_updated)


class DateSchemaMixin:
    created_on = auto_field(dump_only=True)
    last_updated = auto_field(dump_only=True)
