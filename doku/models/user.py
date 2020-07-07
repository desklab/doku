from __future__ import annotations

from typing import Optional
import json
import secrets
from itsdangerous.encoding import base64_encode, base64_decode

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash, pbkdf2_hex
from flask import session, request, current_app

from doku.models import db


class User(db.Model):
    """User Model
    """

    __tablename__ = "doku_user"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    username = db.Column(db.String(48), nullable=False, unique=True)
    name = db.Column(db.String(48), nullable=True, unique=False, default="")
    email = db.Column(db.String(48), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.set_password(kwargs.pop("password"))
        super().__init__(*args, **kwargs)

    @staticmethod
    def _hash_password(password):
        return generate_password_hash(password.encode(), salt_length=12).encode()

    @staticmethod
    def _hash_token(token: str):
        salt = current_app.config.get("API_TOKEN_SALT", "salty_token")
        return pbkdf2_hex(token, salt)

    def set_password(self, password):
        self.password = self._hash_password(password)

    def check_password(self, password):
        return check_password_hash(self.password.decode(), password)

    @property
    def token(self):
        r = current_app.redis
        token = secrets.token_urlsafe(current_app.config.get("API_TOKEN_LENGTH", 32))
        prefix = current_app.config.get("API_TOKEN_STORAGE_PREFIX", "doku_api_token_")
        key = self._hash_token(token)
        value = json.dumps({
            "user": self.username,
            "id": self.id,
            "name": self.name
        })
        expires_in = current_app.config.get("API_TOKEN_STORAGE_EXPIRATION", 3600)
        r.setex(
            name=f"{prefix}{key}",
            time=expires_in,
            value=value
        )
        return {
            "token": base64_encode(token).decode("utf-8"),
            "expires_in": expires_in
        }


    @classmethod
    def authenticate(cls, email: str = "", password: str = "") -> Optional[User]:
        try:
            user: cls = db.session.query(cls).filter_by(email=email).one()
        except NoResultFound:
            return None
        if user.check_password(password):
            return user
        else:
            return None


    @classmethod
    def token_auth(cls, token: str) -> Optional[dict]:
        if "Bearer" not in token:
            return None
        token = base64_decode(token.lstrip("Bearer ")).decode("utf-8")
        r = current_app.redis
        prefix = current_app.config.get("API_TOKEN_STORAGE_PREFIX", "doku_api_token_")
        key = cls._hash_token(token)
        result = r.get(f"{prefix}{key}")
        if result is None:
            return None
        else:
            return json.loads(result)
