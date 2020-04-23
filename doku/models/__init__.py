from datetime import datetime

from flask_babel import format_timedelta, format_datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import auto_field

db = SQLAlchemy(session_options={"autoflush": False})


class DateMixin:
    created_on = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now
    )
    last_updated = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    )

    @property
    def last_updated_timedelta(self):
        return format_timedelta(datetime.now() - self.last_updated)

    @property
    def last_updated_format(self):
        return format_datetime(self.last_updated)


class DateSchemaMixin:
    created_on = auto_field(dump_only=True)
    last_updated = auto_field(dump_only=True)
