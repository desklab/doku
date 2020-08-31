import markdown
from doku.utils.markdown.extensions import RootClassExtension


def compile_content(content: str, css_class: str, use_markdown: bool) -> str:
    if content is None or content == "":
        # In previous versions, the content was set to ""
        # However, this will trigger a recursive function call and
        # should thus be avoided
        return ""
    else:
        if use_markdown:
            return markdown.markdown(
                content,
                extensions=[
                    RootClassExtension(root_class=css_class),
                    "codehilite",
                    "fenced_code",
                ],
            )
        else:
            return content
