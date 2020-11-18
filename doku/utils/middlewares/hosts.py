from werkzeug.exceptions import BadHost
from werkzeug.wrappers import Response
from flask import Flask


class host_middleware:
    """Host Middleware"""

    LOG_MESSAGE = "No host provided. Skip host middleware"

    def __init__(self, app: Flask):
        self._app = app
        self._allowed_hosts = self._app.config.get("ALLOWED_HOSTS", None)
        if self._allowed_hosts is None:
            self._app.logger.warning(self.LOG_MESSAGE)
            return
        self._next = self._app.wsgi_app
        self._app.wsgi_app = self.middleware

    def middleware(self, environ, start_response):
        if environ["SERVER_NAME"] not in self._allowed_hosts:
            return BadHost()(environ, start_response)
        return self._next(environ, start_response)
