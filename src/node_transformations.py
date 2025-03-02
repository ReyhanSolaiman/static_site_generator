from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
    
def text_node_to_html_node(text_node):
    TAG_MAPPING = {
        "text": None,
        "bold": "b",
        "italic": "i",
        "code": "code",
    }
    if text_node.text_type.value == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type.value == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type.value in TAG_MAPPING:
        return LeafNode(TAG_MAPPING[text_node.text_type.value], text_node.text)
    raise Exception(f"invalid TextType: {text_node.text_type.value}")

            