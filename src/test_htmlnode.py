import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("a", "child", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com">child</a></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_dynamic_depth(self):
        depth = 5
        child = LeafNode("span", "Innermost")
        for _ in range(depth):
            child = ParentNode("div", [child])
        node = child
        self.assertEqual(
            node.to_html(),
            "<div><div><div><div><div><span>Innermost</span></div></div></div></div></div>"
            )
    
    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()
    
    def test_to_html_none_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("span", None)
            parent_node.to_html()

    def test_to_html_empty_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("span", [])
            node.to_html()

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(), 
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            )
        
    def test_to_html_combine_parent_children(self):
        grandchild = LeafNode("span", "grandchild")
        child = ParentNode("p", [LeafNode("b", "bold text"), grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><p><b>bold text</b><span>grandchild</span></p></div>")


    

if __name__ == "__main__":
    unittest.main()