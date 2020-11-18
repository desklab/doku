from jinja2 import Environment, meta
from jinja2 import Template as Jinja2Template
from jinja2 import TemplateSyntaxError
from marshmallow import ValidationError


def validate_template(template_source: str) -> bool:
    """Validate Template

    Tries to validate a template by parsing the source, finding
    all undeclared variables and then supplying default strings to all
    variables while rendering the final HTML. Checks are performed at
    each step that might fail.

    :param template_source: String containing HTML/Jinja2 source
    :returns: True if everything worked fine
    :raises: ValidationError on failure
    """
    env = Environment()
    try:
        content = env.parse(template_source)
    except TemplateSyntaxError as e:
        raise ValidationError(message=str(e), field_name="source")
    variables = meta.find_undeclared_variables(content)
    context = {variable_name: "Foo Bar" for variable_name in variables}
    try:
        template = Jinja2Template(template_source)
        template.render(**context)
    except Exception as e:  # noqa
        raise ValidationError(message=str(e), field_name="source")
    return True
