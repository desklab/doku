from doku.tests import DokuTest
from doku.utils.middlewares.csrf import csrf


class CSRFTest(DokuTest):

    def test_csrf_masking(self):
        for i in range(10000):
            secret = csrf._create_string()
            masked = csrf._mask(secret)
            res = csrf._unmask(masked)
            self.assertEqual(secret, res)
