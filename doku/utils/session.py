"""
doku Sessions
~~~~~~~~~~~~~

Flask-based sessions used for doku

.. note::

    Some of this code has been adopted from a project called
    ``flask-session`` by Shipeng Feng

"""
import json
import secrets
from json import JSONDecodeError
from typing import List

from flask import Flask, Response
from flask.helpers import total_seconds
from werkzeug.exceptions import Unauthorized
from flask.sessions import SessionInterface, SessionMixin
from redis import Redis
from werkzeug.datastructures import CallbackDict
from itsdangerous import Signer, BadSignature, want_bytes

from doku.utils import EMPTY
from doku.models.user import User


class Session(CallbackDict, SessionMixin):
    @staticmethod
    def _on_update(self):
        """On update

        In this context, ``_on_update`` is static. However, looking at
        :class:`CallbackDict` reveals, that ``on_update`` is passed the
        object instance ``self``.
        """
        self.modified = True

    def __init__(self, initial=None, sid=None, permanent=None):
        super(Session, self).__init__(initial=initial, on_update=self._on_update)
        self.sid = sid
        if permanent is not None:
            self.permanent = permanent
        self.modified = False

    @property
    def authenticated(self) -> bool:
        return self.get("authenticated", False)

    @authenticated.setter
    def authenticated(self, set_value: bool):
        self["authenticated"] = set_value

    @property
    def nosave(self) -> bool:
        return self.get("_nosave", False)

    @nosave.setter
    def nosave(self, set_value: bool):
        self["_nosave"] = set_value


class RedisSessionInterface(SessionInterface):
    """Redis Session Interface

    A session interface for flask using a Redis backend as storage

    :param app: Required for the use of ``secret_key`` while signing
    :param redis: A Redis instance used to connect to the server
    :param prefix: Prefix to distinguish different keys in Redis
    :param session_class: A class:`flask.sessions.SessionMixin` type,
        used to save the actual session instance.
    :param permanent: Whether the session should be permanent
    """

    _empty = EMPTY
    _KEY_LENGTH = 32
    _serializer = json

    def __init__(
        self,
        app: Flask,
        redis: Redis,
        prefix: str = "session_",
        session_class: type(SessionMixin) = Session,
        permanent: bool = True,
    ):
        self._app = app
        self._redis: Redis = redis
        self._signer: Signer = Signer(
            self._app.secret_key,
            key_derivation="hmac",
            salt=app.config.get("SESSION_SALT", "salty-session"),
        )
        self.prefix: str = prefix
        self.session_class = session_class
        self.permanent = permanent

    def open_session(self, app, request) -> SessionMixin:
        sid_signed = request.cookies.get(app.session_cookie_name, None)
        if sid_signed in self._empty:
            return self.empty_session()
        try:
            # Un-sign the signed session id
            sid_bytes = self._signer.unsign(sid_signed)
            sid = sid_bytes.decode()
        except BadSignature:
            app.logger.info(
                "Session cookie has bad signature. A new session will be created"
            )
            return self.empty_session()
        # Get the raw session instance from redis
        raw_session = self._redis.get(self.get_key(sid))
        if raw_session not in self._empty:
            try:
                session = self._serializer.loads(raw_session)
                return self.session_class(initial=session, sid=sid)
            except (TypeError, JSONDecodeError) as e:
                app.logger.info(f"Failed to load session: {e}")
                return self.empty_session()
        else:
            app.logger.info("Session not found. A new session will be created")
            return self.empty_session()

    def empty_session(self) -> SessionMixin:
        """Create new empty Session"""
        return self.session_class(sid=self._get_unique_sid(), permanent=self.permanent)

    def save_session(self, app: Flask, session: Session, response: Response):
        if session is None:
            # This should never be the case
            return
        if session.nosave:
            # Prevent session from being saved
            # E.g. when using token authentication
            return
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            # ``not session`` equates to an empty session
            if session.modified or not session.authenticated:
                # The session has been modified. This indicates, that
                # a session has been invalidated by deleting it or
                # removing authentication. Thus, we try to remove any
                # traces
                self._redis.delete(self.get_key(session.sid))
                response.delete_cookie(
                    app.session_cookie_name, domain=domain, path=path
                )
            return

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        samesite = self.get_cookie_samesite(app)

        raw_session = self._serializer.dumps(session)
        # ``setex`` is used to create an entry that expires
        self._redis.setex(
            name=self.get_key(session.sid),
            time=app.permanent_session_lifetime,
            value=raw_session,
        )
        sid_signed: bytes = self._signer.sign(session.sid)
        response.set_cookie(
            app.session_cookie_name,
            sid_signed.decode("utf-8"),
            domain=domain,
            path=path,
            httponly=httponly,
            expires=expires,
            secure=secure,
            samesite=samesite,
        )

    def _get_unique_sid(self) -> str:
        """Get Unique Session ID

        This will continually generate a new session ID using the
        :meth:`secrets.token_urlsafe` method using ``_KEY_LENGTH`` as
        default size (in bytes) while checking, if the ID already exists
        in Redis. This will avoid a collision of the unique constraint.
        """
        sid = secrets.token_urlsafe(self._KEY_LENGTH)
        while self._redis.exists(self.get_key(sid)):
            sid = secrets.token_urlsafe(self._KEY_LENGTH)
        return sid

    def get_key(self, sid: str) -> str:
        return self.prefix + sid
