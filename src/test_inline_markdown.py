from textnode import TextNode, TextType
import unittest
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            split_nodes_image([node])
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            split_nodes_link([node])
        )

    def test_split_images_not_text(self):
        node = TextNode("This is not text but bold", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is not text but bold", TextType.BOLD)
            ],
            split_nodes_image([node])
        )

    def test_split_links_not_text(self):
        node = TextNode("This is not text but bold", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is not text but bold", TextType.BOLD)
            ],
            split_nodes_link([node])
        )
    
    def test_split_images_no_image(self):
        node = TextNode("This is text without an image", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("This is text without an image", TextType.TEXT)
            ],
            split_nodes_image([node])
        )

    def test_split_images_no_link(self):
        node = TextNode("This is text without an link", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("This is text without an link", TextType.TEXT)
            ],
            split_nodes_link([node])
        )

    def test_split_images_multiple_nodes(self):
        node_1 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node_2 = TextNode("This is text with another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            split_nodes_image([node_1, node_2])
        )

    def test_split_links_multiple_nodes(self):
        node_1 = TextNode("This is text with a [to boot dev](https://www.boot.dev)", TextType.TEXT)
        node_2 = TextNode("This is text with another [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is text with another ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            split_nodes_link([node_1, node_2])
        )

    def test_split_image_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            split_nodes_image([node])
        )

    def test_split_link_only(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ],
            split_nodes_link([node])
        )

if __name__ == "__main__":
    unittest.main()