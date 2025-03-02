from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from node_transformations import text_node_to_html_node
import unittest

class TestNodeTransformations(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is alt text", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is alt text"}
        )

    def test_link(self):
        node = TextNode("This is link text", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is link text")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.boot.dev"}
        )

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_invalid_text_type(self):
        class UnsupportedType:
            value = "unsupported"
        node = TextNode("Invalid text type", UnsupportedType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(
            str(context.exception),
            "invalid TextType: unsupported"
        )

if __name__ == "__main__":
    unittest.main()