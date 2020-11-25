from flask import jsonify, json
from werkzeug.exceptions import BadRequest

from doku.tests import DokuTest
from doku.models import db
from doku.models.base import Document, Template


class VariableTest(DokuTest):
    def test_valid_filename(self):
        with self.app.app_context():
            template = Template(name="Foo Test Template")
            doc = Document(name="Foo:Bar Hello World", author=self.user)
            doc.template = template
            db.session.add(template)
            db.session.add(doc)
            db.session.commit()
            self.assertEqual(doc.filename, "foobar_hello_world")
