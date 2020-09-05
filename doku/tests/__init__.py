import unittest

from doku import create_app
from doku.models import db
from doku.models.user import User


class DokuTest(unittest.TestCase):

    PASSWORD = "CorrectHorseBatteryStaple"
    EMAIL = "test@doku.test"

    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all(app=self.app)
            user = User()
            user.set_password(self.PASSWORD)
            user.name = "Test User"
            user.username = "testuser"
            user.email = self.EMAIL
            db.session.add(user)
            db.session.commit()
            self.user = user

    def tearDown(self):
        pass
