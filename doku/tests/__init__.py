import unittest

from doku import create_app


class DokuTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client()

    def tearDown(self):
        pass
