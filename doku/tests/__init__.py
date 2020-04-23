import unittest

from doku import create_app


class DokuTest(unittest.TestCase):
    def setUp(self):
        app = create_app(test=True)
        self.app = app.test_client()

    def tearDown(self):
        pass
