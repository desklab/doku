import unittest

import markdown

from doku.utils.markdown.extensions import RootClassExtension
from doku.utils.markdown import compile_content


class MarkdownTest(unittest.TestCase):
    def test_markdown_root_class(self):
        root_class = "foo"
        source = """Hello **World**

        Test
        """
        content = markdown.markdown(
            source,
            extensions=[
                RootClassExtension(root_class=root_class),
                "codehilite",
                "fenced_code",
            ],
        )
        self.assertIn('class="foo"', content)
        self.assertTrue(content.startswith('<div class="foo">'))

    def test_markdown_bleach(self):
        script_tag = "<script></script>"
        result = compile_content(script_tag, None, False)
        self.assertNotIn("<script>", result)
        result = compile_content(script_tag, None, True)
        self.assertNotIn("<script>", result)

    def test_markdown_katex(self):
        katex_formula = r"""```math
\int_0^\pi \sin(x)dx
```"""
        result = compile_content(katex_formula, None, True)
        self.assertIn('class="katex"', result)
