import logging

from werkzeug.exceptions import BadHost
from flask import jsonify

from doku import create_app
from doku.tests import DokuTest
from doku.utils.middlewares.hosts import host_middleware


class HostTest(DokuTest):

    def setUp(self):
        pass

    def _setup_with_config(self, config):
        self.app = create_app(test=True, additional_config=config)
        self.client = self.app.test_client()

        @self.app.route("/foo")
        def test_route():
            return jsonify({"success": True})

    def test_missing_hosts(self):
        config = {
            'ALLOWED_HOSTS': []  # No hosts allowed
        }
        self._setup_with_config(config)
        resp = self.client.get("/foo")
        self.assertEqual(resp.status_code, BadHost.code)

    def test_no_hosts(self):
        config = {
            'ALLOWED_HOSTS': None  # All hosts allowed
        }
        with self.assertLogs(logger="doku", level=logging.WARNING) as logs:
            self._setup_with_config(config)
        message = f"WARNING:doku:{host_middleware.LOG_MESSAGE}"
        self.assertIn(message, logs.output)
        resp = self.client.get("/foo")
        self.assertEqual(resp.status_code, 200)

    def test_localhost(self):
        config = {
            'ALLOWED_HOSTS': "localhost"
        }
        self._setup_with_config(config)
        resp = self.client.get("/foo")
        self.assertEqual(resp.status_code, 200)

    def test_other_host(self):
        config = {
            'ALLOWED_HOSTS': "example.org"
        }
        self._setup_with_config(config)
        resp = self.client.get("/foo")
        self.assertEqual(resp.status_code, BadHost.code)
