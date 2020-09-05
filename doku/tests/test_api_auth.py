from base64 import b64encode, b64decode
import binascii

from flask import jsonify, json, url_for
from werkzeug.exceptions import BadRequest, Unauthorized

from doku.tests import DokuTest
from doku.models import db


class APIAuthTest(DokuTest):

    def test_login(self):
        login = b64encode(f"{self.EMAIL}:{self.PASSWORD}".encode()).decode()
        headers = {"Authorization": f"Basic {login}"}
        res = self.client.post("/api/v1/login", headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_invalid_login(self):
        login = "ThisIsInvalidBase64"
        with self.assertRaises(binascii.Error):
            b64decode(login)
        headers_invalid_b64 = {"Authorization": f"Basic {login}"}
        res = self.client.post("/api/v1/login", headers=headers_invalid_b64)
        self.assertEqual(res.status_code, BadRequest.code)
        json_res = json.loads(res.data)
        self.assertEqual(json_res["error"], "No authorization provided")

        login_wrong = b64encode(f"{self.EMAIL}:WRONGPASSWORD".encode()).decode()
        headers_wrong = {"Authorization": f"Basic {login_wrong}"}
        res = self.client.post("/api/v1/login", headers=headers_wrong)
        self.assertEqual(res.status_code, Unauthorized.code)

    def test_api_token(self):
        login = b64encode(f"{self.EMAIL}:{self.PASSWORD}".encode()).decode()
        headers = {"Authorization": f"Basic {login}"}
        res = self.client.post("/api/v1/login", headers=headers)
        res_json = json.loads(res.data)
        token_type = res.json["token_type"]
        access_token = res.json["access_token"]

        auth_headers = {"Authorization": f"{token_type} {access_token}"}
        res_get = self.client.get("/api/v1/document/", headers=auth_headers)
        self.assertEqual(res_get.status_code, 200)
        self.assertNotIn("Set-Cookie", res_get.headers)

    def test_unauthorized(self):
        login = b64encode(f"{self.EMAIL}:{self.PASSWORD}".encode()).decode()
        headers = {"Authorization": f"Basic {login}"}
        res = self.client.post("/api/v1/document/", headers=headers)
        self.assertEqual(res.status_code, Unauthorized.code)
        json_res = json.loads(res.data)
        self.assertEqual(json_res["error"], "You need to login first")
