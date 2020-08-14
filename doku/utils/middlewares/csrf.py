import hashlib
import secrets
import string
from typing import List, Optional

from flask import Flask, request, g
from flask.wrappers import Response
from itsdangerous import Signer, BadSignature
from werkzeug.exceptions import NotFound, BadRequest


class CSRFMiddleware:
    DEFAULT_EXCLUDED_METHODS: List[str] = ["GET", "HEAD", "OPTIONS", "TRACE"]
    CSRF_TOKEN_CHARS = string.ascii_letters + string.digits

    def __init__(self, app: Optional[Flask] = None):
        self._app = app
        self._exemptions = []
        self._config = {}
        self._signer: Optional[Signer] = None
        if self._app is not None:
            self.init_app(self._app)

    def exempt(self, view):
        """Exempt Decorator

        Use this method as a decorator. Note that it has to be used with
        an instance of :class:`CSRFMiddleware`!
        """
        self._exemptions.append(view)
        return view

    def init_app(self, app):
        self._app = app
        self._config = self._get_config(app.config)
        self._signer = Signer(
            self._app.secret_key,
            salt="csrf_salty_key",
            key_derivation="hmac",
            digest_method=hashlib.sha256,
        )

        @self._app.before_request
        def _csrf_skip_exemptions():
            if request.endpoint == "static":
                g._is_csrf_exemption = True
                g._csrf_should_set = False
                return
            try:
                view = app.view_functions.get(request.endpoint)
                g._is_csrf_exemption = view in self._exemptions
            except NotFound:
                g._is_csrf_exemption = False

        @self._app.before_request
        def _csrf_protection():
            if g._is_csrf_exemption:
                return
            if request.method in self._config["EXCLUDED_METHODS"]:
                return
            if request.headers.get("Authorization", None) is not None:
                # Basic Auth or Token based Authentication
                return
            # Retrieve CSRF token from header or request data
            csrf_token = request.headers.get(self._config["HEADER_NAME"])
            if csrf_token is None:
                data = request.values.copy()
                if request.json is not None:
                    data.update(request.json)
                csrf_token = data.get("csrf_token", None)
            if csrf_token is None:
                raise BadRequest(
                    "CSRF token missing! Make sure that a field "
                    'called "csrf_token" is present.'
                )

            # Retrieve CSRF cookie
            csrf_cookie = request.cookies.get(self._config["COOKIE_NAME"])
            if csrf_cookie is None:
                raise BadRequest(
                    "CSRF cookie missing! " "Make sure that it is present."
                )
            try:
                unsigned_token = self._signer.unsign(csrf_token)
                unsigned_token = unsigned_token.decode()
                unsigned_cookie = self._signer.unsign(csrf_cookie)
                unsigned_cookie = unsigned_cookie.decode()
            except BadSignature:
                raise BadRequest("Bad CSRF token signature")
            token, random_token = unsigned_token.split(".")
            token_cookie, random_token_cookie = unsigned_token.split(".")
            try:
                secret = self._unmask(token)
                secret_cookie = self._unmask(token_cookie)
            except:
                raise BadRequest("Invalid CSRF token")
            if not secret == secret_cookie:
                raise BadRequest("Invalid CSRF token")
            # All tests passed
            # Continue with request
            return

        @self._app.context_processor
        def inject_csrf_context():
            return dict(create_csrf_token=self.create_csrf_token)

        @self._app.after_request
        def _set_csrf_cookie(response: Response):
            if not getattr(g, "_csrf_should_set", False):
                return response
            token = self._mask(g._csrf_secret)
            random_token = self._create_string()
            signed_token = self._signer.sign(f"{token}.{random_token}").decode()
            response.set_cookie(
                self._config["COOKIE_NAME"],
                value=signed_token,
                httponly=False,
                secure=self._config["COOKIE_SECURE"],
                samesite=self._config["COOKIE_SAMESITE"],
                max_age=None,
            )
            return response

    @staticmethod
    def _get_config(app_config) -> dict:
        """Get config

        Create config :type:`dict` from Flask app config. This is also
        where defaults are set.

        Available configurations:

          - `CSRF_COOKIE_NAME`
          - `CSRF_COOKIE_SECURE`
          - `CSRF_EXCLUDED_METHODS`
          - `CSRF_TOKEN_LENGTH`

        """
        _config = {
            "COOKIE_NAME": app_config.get("CSRF_COOKIE_NAME", "csrf_token"),
            "COOKIE_SECURE": app_config.get("CSRF_COOKIE_SECURE", False),
            "COOKIE_SAMESITE": app_config.get("CSRF_COOKIE_SAMESITE", "Lax"),
            "HEADER_NAME": app_config.get("CSRF_HEADER_NAME", "X-CSRF-TOKEN"),
            "EXCLUDED_METHODS": app_config.get(
                "CSRF_EXCLUDED_METHODS", CSRFMiddleware.DEFAULT_EXCLUDED_METHODS
            ),
            "TOKEN_LENGTH": app_config.get("CSRF_TOKEN_LENGTH", 32),
        }
        return _config

    def _create_string(self):
        """Create a random string

        """
        length = self._config["TOKEN_LENGTH"]
        return secrets.token_hex(length)

    def _mask(self, secret):
        length = self._config["TOKEN_LENGTH"]
        mask = self._create_string()
        cipher = int(secret, base=16) ^ int(mask, base=16)
        cipher_hex = cipher.to_bytes(length=length, byteorder="big").hex()
        return f"{cipher_hex}{mask}"

    def _unmask(self, token):
        length = self._config["TOKEN_LENGTH"]
        as_bytes = bytes.fromhex(token)
        cipher = bytes.hex(as_bytes[:length])
        mask = bytes.hex(as_bytes[length:])
        secret_raw = int(cipher, base=16) ^ int(mask, base=16)
        return secret_raw.to_bytes(length=length, byteorder="big").hex()

    def create_csrf_token(self, output=True) -> str:
        g._csrf_should_set = True
        secret = self._create_string()
        g._csrf_secret = secret
        if output:
            token = self._mask(secret)
            random_token = self._create_string()
            return self._signer.sign(f"{token}.{random_token}").decode()
        else:
            return ""


csrf = CSRFMiddleware()
