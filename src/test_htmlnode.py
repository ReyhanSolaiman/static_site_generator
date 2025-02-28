import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()