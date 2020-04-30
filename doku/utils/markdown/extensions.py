from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class RootClassTreeprocessor(Treeprocessor):
    def __init__(self, md=None, root_class=None):
        super(RootClassTreeprocessor, self).__init__(md=md)
        self.root_class = root_class

    def run(self, root):
        if self.root_class not in ['', None]:
            root.set('class', self.root_class)


class RootClassExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {'root_class': ['', 'CSS class for root element']}
        super(RootClassExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        if self.getConfig('root_class') in ['', None]:
            return
        _processor = RootClassTreeprocessor(
            md=md, root_class=self.getConfig('root_class')
        )
        md.stripTopLevelTags = False
        md.treeprocessors.register(_processor, 'root_tree_class', 15)
