from typing import List, Optional

import bleach
import markdown
import markdown_katex

from doku.utils.markdown.extensions import RootClassExtension

# fmt: off
BLEACH_ALLOWED_TAGS: List[str] = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "b", "i", "strong", "em", "tt",
    "p", "br",
    "span", "div", "blockquote", "code", "pre", "hr",
    "ul", "ol", "li", "dd", "dt",
    "img",
    "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    "a",
    "sub", "sup",
]

BLEACH_ALLOWED_ATTRS: dict = {
    "*": ["class", "id", "style"],
    "img": ["src", "alt", "title", "width", "height"],
    "a": ["href", "alt", "title"],
}

BLEACH_ALLOWED_PROTOCOLS = ["http", "https", "dokures"]

# fmt: on


def compile_content(content: str, css_class: Optional[str], use_markdown: bool) -> str:
    if content is None or content == "":
        # In previous versions, the content was set to ""
        # However, this will trigger a recursive function call and
        # should thus be avoided
        return ""
    else:
        # Make sure we sanitize content before saving it as
        # ``compiled_content`` even if we do not use markdown.
        content = bleach.clean(content,
                               tags=BLEACH_ALLOWED_TAGS,
                               attributes=BLEACH_ALLOWED_ATTRS,
                               protocols=BLEACH_ALLOWED_PROTOCOLS)
        if use_markdown:
            return markdown.markdown(
                content,
                extensions=[
                    RootClassExtension(root_class=css_class),
                    "codehilite",
                    "fenced_code",
                    "tables",
                    "markdown_katex",
                ],
                extension_configs={
                    "markdown_katex": {
                        "no_inline_svg": True,  # needed for WeasyPrint
                        "insert_fonts_css": False,
                    },
                },
            )
        else:
            return content
