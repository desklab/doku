import unittest

from marshmallow import ValidationError

from doku.models.schemas import VariableSchema, TemplateSchema


class TestJinja(unittest.TestCase):
    def setUp(self):
        self.variable_schema = VariableSchema(load_instance=False)
        self.template_schema = TemplateSchema(load_instance=False)

    def test_invalid_variable_name(self):
        with self.assertRaises(ValidationError):
            self.variable_schema.load({"id": 42, "name": "foo-bar", "document_id": 0})
        with self.assertRaises(ValidationError):
            self.variable_schema.load({"id": 42, "name": "bar\nfoo", "document_id": 0})
        with self.assertRaises(ValidationError):
            self.variable_schema.load({"id": 42, "name": "foo bar", "document_id": 0})
        with self.assertRaises(ValidationError):
            self.variable_schema.load({"id": 42, "name": [], "document_id": 0})
        with self.assertRaises(ValidationError):
            self.variable_schema.load({"id": 42, "name": "", "document_id": 0})

    def test_valid_variable_name(self):
        self.variable_schema.load({"id": 42, "name": "foo", "document_id": 0})
        self.variable_schema.load({"id": 42, "name": "foo_bar", "document_id": 0})
        self.variable_schema.load({"id": 42, "name": "foo42_bar", "document_id": 0})

    def test_invalid_template(self):
        with self.assertRaises(ValidationError):
            self.template_schema.load({"id": 42, "source": "{{ variable-name }}"})
        with self.assertRaises(ValidationError):
            self.template_schema.load({"id": 42, "source": "{{ variable name }}"})

    def test_valid_template(self):
        self.template_schema.load({"id": 42, "source": "{{ variable_name }}"})
