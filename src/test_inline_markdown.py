import unittest


from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)
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

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ],
            extract_markdown_images(text),
        )

    def test_extract_markdown_images__multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(text),
        )

    def test_extract_markdown_images__no_images(self):
        text = "This is text with no images"
        self.assertEqual([], extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
            ],
            extract_markdown_links(text),
        )

    def test_extract_markdown_links__multilple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )

    def test_extract_markdown_links__no_links(self):
        text = "This is text with no links"
        self.assertEqual([], extract_markdown_links(text))

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) image",
            TextType.TEXT,
        )

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" image", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_nodes_image__starts_with(self):
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) image",
            TextType.TEXT,
        )

        self.assertEqual(
            [
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" image", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_nodes_image__ends_with(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            split_nodes_image([node]),
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [duck duck go](https://duckduckgo.com) and [google](https://google.com) links",
            TextType.TEXT,
        )

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("duck duck go", TextType.LINK, "https://duckduckgo.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("google", TextType.LINK, "https://google.com"),
                TextNode(" links", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_nodes_link__starts_with(self):
        node = TextNode(
            "[duck duck go](https://duckduckgo.com) and [google](https://google.com) links",
            TextType.TEXT,
        )

        self.assertEqual(
            [
                TextNode("duck duck go", TextType.LINK, "https://duckduckgo.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("google", TextType.LINK, "https://google.com"),
                TextNode(" links", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_nodes_link__ends_with(self):
        node = TextNode(
            "This is text with a [duck duck go](https://duckduckgo.com) and [google](https://google.com)",
            TextType.TEXT,
        )

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("duck duck go", TextType.LINK, "https://duckduckgo.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("google", TextType.LINK, "https://google.com"),
            ],
            split_nodes_link([node]),
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* and _other italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("other italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
