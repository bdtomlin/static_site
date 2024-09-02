import unittest

from markdown_blocks import markdown_to_blocks


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
        This is the first block.

        This is the second block.
        This is the second block, still.



        This is block 3.

        """
        expected = [
            "This is the first block.",
            "This is the second block.\n        This is the second block, still.",
            "This is block 3.",
        ]
        actual = markdown_to_blocks(markdown)
        self.assertEqual(expected, actual)

    def test_markdown_to_blocks__empty(self):
        markdown = ""
        expected = []
        actual = markdown_to_blocks(markdown)
        self.assertEqual(expected, actual)
