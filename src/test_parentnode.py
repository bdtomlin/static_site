import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        children = [
            LeafNode("p", "value", {"class": "any"}),
            LeafNode("p", "value", {"class": "any"}),
        ]
        parent_node = ParentNode("div", children, {"class": "any"})
        self.assertEqual(
            '<div class="any"><p class="any">value</p><p class="any">value</p></div>',
            parent_node.to_html(),
        )

    def test_to_html_with_nested_children(self):
        c5 = LeafNode("p", "child 5", {"id": "c5"})
        c4 = LeafNode("p", "child 4", {"id": "c4"})
        c3 = ParentNode("div", [c4, c5], {"id": "c3"})
        c2 = ParentNode("div", [c3], {"id": "c2"})
        p = ParentNode("div", [c2], {"id": "p"})

        expected = '<div id="p"><div id="c2"><div id="c3"><p id="c4">child 4</p><p id="c5">child 5</p></div></div></div>'

        self.assertEqual(expected, p.to_html())

    def test_to_html_with_invalid_child(self):
        invalid_child = LeafNode("child")
        parent = ParentNode("div", [invalid_child], {"id": "parent"})

        self.assertRaises(ValueError, parent.to_html)

    def test_tagless_to_html(self):
        value = "some value"
        node = LeafNode(value=value)
        self.assertEqual(value, node.to_html())

    def test_to_html_raises_without_chidren(self):
        node = ParentNode("div")
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_raises_without_tag(self):
        node = ParentNode()
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
