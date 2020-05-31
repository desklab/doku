from werkzeug.security import generate_password_hash, check_password_hash

from doku.models import db


class User(db.Model):
    """User Model
    """

    __tablename__ = "doku_user"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    username = db.Column(db.String(48), nullable=False, unique=True)
    email = db.Column(db.String(48), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.set_password(kwargs.pop("password"))
        super().__init__(*args, **kwargs)

    @staticmethod
    def _hash_password(password):
        return generate_password_hash(password.encode(), salt_length=12).encode()

    def set_password(self, password):
        self.password = self._hash_password(password)

    def check_password(self, password):
        return check_password_hash(self.password.decode(), password)

    def authenticate(self, request):
        pass
