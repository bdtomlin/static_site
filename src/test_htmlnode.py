import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_raises(self):
        node = HTMLNode("p", "value", [], {"class": "parent"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("p", "value", [], {"class": "xxx", "id": "yyy"})

        self.assertEqual(node.props_to_html(), ' class="xxx" id="yyy"')

    def test__repr__(self):
        node = HTMLNode("p", "value", [], {"id": "any"})

        self.assertEqual(
            str(node), "HTMLNode(tag=p, value=value, children=[], props={'id': 'any'})"
        )


if __name__ == "__main__":
    unittest.main()
