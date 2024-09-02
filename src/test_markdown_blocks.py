import unittest

from markdown_blocks import block_to_block_type, markdown_to_blocks


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

    def test_block_to_block_type__heading(self):
        for i in range(6):
            n = i + 1
            hshs = "#" * n
            block = f"{hshs} Some Text"
            expected = f"h{n}"
            actual = block_to_block_type(block)
            self.assertEqual(expected, actual)

    def test_block_to_block_type__code(self):
        block = "```here's the code```"
        expected = "code"
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type__quote(self):
        block = "> this\n> is\n> a quote"
        expected = "quote"
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type__not_quote(self):
        block = "> this\n is not\n> a quote"
        not_expected = "quote"
        actual = block_to_block_type(block)
        self.assertNotEqual(not_expected, actual)

    def test_block_to_block_type__ul(self):
        block = "* this\n* is\n* a ul"
        expected = "ul"
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type__not_ul(self):
        block = "* this\n is not\n* a ul"
        not_expected = "quote"
        actual = block_to_block_type(block)
        self.assertNotEqual(not_expected, actual)

    def test_block_to_block_type__ol(self):
        block = "1. this\n2. is\n3. an ol"
        expected = "ol"
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type__not_ol(self):
        block = "1. this\n is not\n3. not an ol"
        not_expected = "ol"
        actual = block_to_block_type(block)
        self.assertNotEqual(not_expected, actual)

    def test_block_to_block_type__not_ol2(self):
        block = "1. this\n3. is not\n2. not an ol"
        not_expected = "ol"
        actual = block_to_block_type(block)
        self.assertNotEqual(not_expected, actual)
