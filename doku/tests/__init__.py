import unittest

from doku import create_app
from doku.models import db


class DokuTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all(app=self.app)

    def tearDown(self):
        pass
