import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode(props={"href": "https://www.boot.dev/tracks/backend", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html_types(self):
        node = HTMLNode(props={"integer": 5, "boolean": False})
        self.assertEqual(node.props_to_html(), ' integer="5" boolean="False"')

    def test_values(self):
        node = HTMLNode("p", "paragraph text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "paragraph text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("div", "div text", None, {"key": "value"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=div text, children=None, props={'key': 'value'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(), "Hello World")

    def test_leaf_to_html_special_mult_props(self):
        node = LeafNode("a", "Test text", {"href": "https://www.boot.dev/tracks/backend", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev/tracks/backend" target="_blank">Test text</a>')

if __name__ == "__main__":
    unittest.main()