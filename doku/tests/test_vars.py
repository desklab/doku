from flask import jsonify, json
from werkzeug.exceptions import BadRequest

from doku.tests import DokuTest
from doku.models import db
from doku.models.base import Document, Variable, Template


class VariableTest(DokuTest):
    def test_variable_compile(self):
        with self.app.app_context():
            template = Template(name="Foo Test Template")
            doc = Document(name="Foo", author=self.user)
            doc.template = template
            db.session.add(template)
            db.session.add(doc)
            db.session.commit()
            variable = Variable(name="body", document_id=doc.id)
            db.session.add(variable)
            db.session.commit()
            self.assertEqual(variable.content, "")
            self.assertEqual(variable.compiled_content, "")
            variable.content = "Hello **World**"
            db.session.commit()
            self.assertNotEqual(variable.compiled_content, "")
            self.assertEqual(
                variable.compiled_content, "<p>Hello <strong>World</strong></p>"
            )

    def test_variable_raw(self):
        with self.app.app_context():
            template = Template(name="Foo Test Template")
            doc = Document(name="Foo", author=self.user)
            doc.template = template
            db.session.add(template)
            db.session.add(doc)
            db.session.commit()
            variable = Variable(name="body", document_id=doc.id)
            db.session.add(variable)
            db.session.commit()
            self.assertEqual(variable.content, "")
            self.assertEqual(variable.compiled_content, "")
            variable.content = "Hello **World**"
            variable.use_markdown = False
            db.session.commit()
            self.assertNotEqual(variable.compiled_content, "")
            self.assertEqual(variable.compiled_content, variable.content)

    def test_update_document(self):
        with self.app.app_context():
            template = Template(name="Foo Test Template")
            doc = Document(name="Foo", author=self.user)
            doc.template = template
            db.session.add(template)
            db.session.add(doc)
            db.session.commit()

            old_date = doc.last_updated

            variable = Variable(name="body", document_id=doc.id)
            db.session.add(variable)
            db.session.commit()

            self.assertGreater(doc.last_updated, old_date)
