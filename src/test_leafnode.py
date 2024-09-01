import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "value", {"class": "any"})
        self.assertEqual('<p class="any">value</p>', node.to_html())

    def test_tagless_to_html(self):
        value = "some value"
        node = LeafNode(value=value)
        self.assertEqual(value, node.to_html())

    def test_to_html_raises(self):
        node = LeafNode("p")
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
