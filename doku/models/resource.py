import random
import string

from flask import url_for
from sqlalchemy import Index
from werkzeug.utils import secure_filename

from doku.models import db, DateMixin, TSVector


class Resource(db.Model, DateMixin):
    """Resource Model"""

    __tablename__ = "doku_resource"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String(255), unique=False, nullable=False)
    filename = db.Column(db.String(255), unique=True, nullable=False)

    __ts_vector__ = db.Column(
        TSVector(),
        db.Computed(
            "to_tsvector('english', name)",
            persisted=True
        )
    )

    __table_args__ = (
        Index('doku_resource___ts_vector__', __ts_vector__, postgresql_using='gin'),
    )

    @property
    def url(self):
        return url_for("resources.view", resource_id=self.id)


def generate_filename(filename, k=8):
    """Generate (unique) Filename

    Generates a new filename from the given file that is unique. Note
    that this requires a SQLAlchemy session to be present as a query for
    existing filenames is executed at least once.

    :param filename: The original filename. Can be a path
    :param k: Length of additional character
    :returns: Original filename with additional random string of size k
    """
    filename = secure_filename(filename)  # Overwrite insecure filename
    new_name = filename  # Try with original filename first
    while db.session.query(
        Resource.query.filter_by(filename=new_name).exists()
    ).scalar():
        new_name = _random_filename(filename, k=k)
    return new_name


def _random_filename(filename, k=8):
    """Random Filename

    :param filename: The original filename. Can be a path
    :param k: Length of additional character
    :returns: Original filename with additional random string of size k
    """
    filename = filename.split(".", 1)
    salt = "".join(random.choices(string.ascii_lowercase, k=k))
    filename[0] = f"{filename[0]}_{salt}"
    return ".".join(filename)
