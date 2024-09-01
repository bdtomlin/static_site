import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_node_to_html__text(self):
        text = "some text"
        node = TextNode(text, TextType.TEXT)
        expected = LeafNode(value=text).to_html()
        actual = node.text_node_to_html().to_html()
        self.assertEqual(expected, actual)

    def test_text_node_to_html__bold(self):
        text = "some text"
        node = TextNode(text, TextType.BOLD)
        expected = LeafNode("b", value=text).to_html()
        actual = node.text_node_to_html().to_html()
        self.assertEqual(expected, actual)

    def test_text_node_to_html__italic(self):
        text = "some text"
        node = TextNode(text, TextType.ITALIC)
        expected = LeafNode("i", value=text).to_html()
        actual = node.text_node_to_html().to_html()
        self.assertEqual(expected, actual)

    def test_text_node_to_html__code(self):
        text = "some text"
        node = TextNode(text, TextType.CODE)
        expected = LeafNode("code", value=text).to_html()
        actual = node.text_node_to_html().to_html()
        self.assertEqual(expected, actual)

    def test_text_node_to_html__link(self):
        text = "some text"
        node = TextNode(text, TextType.LINK, "#url")
        expected = LeafNode("a", text, {"href": "#url"}).to_html()
        actual = node.text_node_to_html().to_html()
        self.assertEqual(expected, actual)

    def test_text_node_to_html__image(self):
        text = "some text"
        node = TextNode(text, TextType.IMAGE, "/img/i.jpg")
        expected = LeafNode("img", "", {"src": "/img/i.jpg", "alt": text}).to_html()
        actual = node.text_node_to_html().to_html()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
