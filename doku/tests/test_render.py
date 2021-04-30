from flask import url_for

from doku.models import db
from doku.models.base import Document, Template, Variable
from doku.tests import DokuTest


EXAMPLE_TEMPLATE = """<!doctype html>
<html lang="de">
<head>
  <title>{{ title }}</title>
  <meta charset="utf-8">
</head>
<body>
    {{ body }}
</body>
</html>"""


class RenderTest(DokuTest):
    def test_document_render(self):
        with self.app.app_context():
            template = Template(
                name="Plain Test Template", source=EXAMPLE_TEMPLATE  # noqa
            )
            doc = Document(name="Simple Test Document", author=self.user)
            doc.template = template
            db.session.add(template)
            db.session.add(doc)
            db.session.commit()
            # Create Variable
            body_var = Variable(
                name="body", content="Hello **World**", document_id=doc.id  # noqa
            )
            title_var = Variable(
                name="title", use_markdown=False, content="", document_id=doc.id  # noqa
            )
            db.session.add(body_var)
            db.session.add(title_var)
            db.session.commit()
            doc_bytes: bytes = doc.render()
            self.assertTrue(doc_bytes.startswith(b"%PDF-"))  # Magic Numbers of a PDF
