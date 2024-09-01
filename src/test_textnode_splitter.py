import unittest
# import pprint


from textnode_splitter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_split_text_nodes_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_text_nodes_delimiter__multple(self):
        node = TextNode(
            "This is text with a **bold** word and **another bold word**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another bold word", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_text_nodes_delimiter__multiple_nodes(self):
        n1 = TextNode("This is text with a **bold** word", TextType.TEXT)
        n2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([n1, n2], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_text_nodes_delimiter__multiple_types(self):
        node = TextNode(
            "This is text with a **bold** word, an *italic* word, and some `code`",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word, an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word, and some ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_split_text_nodes_delimiter__invalid(self):
        node = TextNode("This is text with a **bold", TextType.TEXT)

        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
