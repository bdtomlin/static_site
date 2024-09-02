import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_to_html_node__text(self):
        text = "some text"
        node = TextNode(text, TextType.TEXT)
        expected = LeafNode(value=text).to_html()
        actual = node.to_html_node().to_html()
        self.assertEqual(expected, actual)

    def test_to_html_node__bold(self):
        text = "some text"
        node = TextNode(text, TextType.BOLD)
        expected = LeafNode("b", value=text).to_html()
        actual = node.to_html_node().to_html()
        self.assertEqual(expected, actual)

    def test_to_html_node__italic(self):
        text = "some text"
        node = TextNode(text, TextType.ITALIC)
        expected = LeafNode("i", value=text).to_html()
        actual = node.to_html_node().to_html()
        self.assertEqual(expected, actual)

    def test_to_html_node__code(self):
        text = "some text"
        node = TextNode(text, TextType.CODE)
        expected = LeafNode("code", value=text).to_html()
        actual = node.to_html_node().to_html()
        self.assertEqual(expected, actual)

    def test_to_html_node__link(self):
        text = "some text"
        node = TextNode(text, TextType.LINK, "#url")
        expected = LeafNode("a", text, {"href": "#url"}).to_html()
        actual = node.to_html_node().to_html()
        self.assertEqual(expected, actual)

    def test_to_html_node__image(self):
        text = "some text"
        node = TextNode(text, TextType.IMAGE, "/img/i.jpg")
        expected = LeafNode("img", "", {"src": "/img/i.jpg", "alt": text}).to_html()
        actual = node.to_html_node().to_html()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
