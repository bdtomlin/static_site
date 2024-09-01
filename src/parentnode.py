from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A tag is required")
        if not self.children:
            raise ValueError("A parent node must have children")

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"

        content = ""
        for child in self.children:
            content += child.to_html()
        return opening_tag + content + closing_tag
