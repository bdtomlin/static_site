import unittest
from markdown_to_html_node import markdown_to_html_node
# from pprint import pp

markdown = """
# Heading 1

This is a paragraph.

* a
* b
* c

another regular paragraph, but
let's make this one multiline
just for fun

1. one
2. two
3. three

> A quote starts
> here and spans
> a few lines.

```
def some_fun():
    return "Hello there"
```

I guess I need a [link](http://duckduckgo.com)
and an ![image](some/img/path)
for good measure
"""

expected = """
<div><h1>Heading 1</h1><p>This is a paragraph.</p><ul><li>a</li><li>b</li><li>c</li></ul><p>another regular paragraph, but
let's make this one multiline
just for fun</p><ol><li>1. one</li><li>2. two</li><li>3. three</li></ol><blockquote>A quote starts
here and spans
a few lines.</blockquote><pre><code>
def some_fun():
    return "Hello there"
</code></pre><p>I guess I need a <a href="http://duckduckgo.com">link</a>
and an <img src="some/img/path" alt="image"></img>
for good measure</p></div>
""".strip()


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        actual = markdown_to_html_node(markdown).to_html()
        self.assertEqual(expected, actual)
