from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url}"

    def text_node_to_html(self):
        match self.text_type:
            case TextType.TEXT.value:
                return LeafNode(value=self.text)
            case TextType.BOLD.value:
                return LeafNode("b", self.text)
            case TextType.ITALIC.value:
                return LeafNode("i", self.text)
            case TextType.CODE.value:
                return LeafNode("code", self.text)
            case TextType.LINK.value:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE.value:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise Exception("invalid text type")
