import unittest

import markdown

from doku.utils.markdown.extensions import RootClassExtension


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
