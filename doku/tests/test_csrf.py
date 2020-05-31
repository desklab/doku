from flask import jsonify, json
from werkzeug.exceptions import BadRequest

from doku.tests import DokuTest
from doku.utils.middlewares.csrf import csrf


class CSRFTest(DokuTest):

    def setUp(self):
        super(CSRFTest, self).setUp()

        @self.app.route('/foo/bar', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def test_route():
            return jsonify({'success': True})
        
        @self.app.route('/foo/token')
        def gen_csrf():
            token = csrf.create_csrf_token()
            return jsonify({'token': token})

    def test_csrf_masking(self):
        for i in range(10000):
            secret = csrf._create_string()
            masked = csrf._mask(secret)
            res = csrf._unmask(masked)
            self.assertEqual(secret, res)

    def test_csrf_endpoint(self):
        header_name = self.app.config.get(
            'CSRF_HEADER_NAME', 'X-CSRF-TOKEN'
        )
        resp = self.client.get('/foo/token')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('token', data)
        token = data['token']

        resp_get = self.client.get('/foo/bar')
        self.assertEqual(resp_get.status_code, 200)

        resp_post_1 = self.client.post('/foo/bar', headers={header_name: '123'})
        self.assertEqual(resp_post_1.status_code, BadRequest.code)
        resp_post_2 = self.client.post('/foo/bar', headers={header_name: token})
        self.assertEqual(resp_post_2.status_code, 200)

        resp_put_1 = self.client.put('/foo/bar', headers={header_name: '123'})
        self.assertEqual(resp_put_1.status_code, BadRequest.code)
        resp_put_2 = self.client.put('/foo/bar', headers={header_name: token})
        self.assertEqual(resp_put_2.status_code, 200)

        resp_del_1 = self.client.delete('/foo/bar',
                                        headers={header_name: '123'})
        self.assertEqual(resp_del_1.status_code, BadRequest.code)
        resp_del_2 = self.client.delete('/foo/bar',
                                        headers={header_name: token})
        self.assertEqual(resp_del_2.status_code, 200)
