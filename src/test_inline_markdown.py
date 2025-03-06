from textnode import TextNode, TextType
import unittest
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        self.assertListEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )
        
    def test_delim_bold_double(self):
        node = TextNode("This text is **bold** and so is **this**", TextType.TEXT)
        self.assertListEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This text is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and so is ", TextType.TEXT),
                TextNode("this", TextType.BOLD)
            ]
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is **bolded word** text", TextType.TEXT)
        self.assertListEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )
 
    def test_delim_bold_italic_code(self):
        node = TextNode("This is **bold**, this is _italic_, and this is `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and this is ", TextType.TEXT),
                TextNode("code", TextType.CODE)
            ]
        )

    def test_invalid_delimiter(self):
        node = TextNode("This is &invalid&", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "&", TextType.BOLD)
        self.assertEqual(
            str(context.exception), 
            "invalid Markdown syntax"
        )

    def test_delim_not_closed(self):
        node = TextNode("This is not closed **bold", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            str(context.exception), 
            "invalid markdown, formatted section not closed"
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ], 
            matches
        )

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"), 
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            matches
        )
        


if __name__ == "__main__":
    unittest.main()