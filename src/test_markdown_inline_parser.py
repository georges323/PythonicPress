import unittest

from markdown_inline_parser import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_links, text_to_textnodes
from textnode import TextNode, TextType

class TestMarkdownInlineParser(unittest.TestCase):
    def test_single_node_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        expected_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_new_nodes)


    def test_single_node_with_multiple_delimiter(self):
        node = TextNode("This is text with a *bold text* word! and this one too *yo yo*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)

        expected_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word! and this one too ", TextType.TEXT),
            TextNode("yo yo", TextType.BOLD),
        ]

        self.assertEqual(new_nodes, expected_new_nodes)

    def test_multiple_nodes_delimiter(self):
        node1 = TextNode("This is text with a *bold text* word! and this one too *yo yo*", TextType.TEXT)
        node2 = TextNode("Already Italics", TextType.ITALICS)
        node3 = TextNode("*Bold Header*", TextType.TEXT)
        node4 = TextNode("[image](www.google.com)", TextType.IMAGE)

        new_nodes = split_nodes_delimiter([node1, node2, node3, node4], "*", TextType.BOLD)

        expected_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word! and this one too ", TextType.TEXT),
            TextNode("yo yo", TextType.BOLD),
            TextNode("Already Italics", TextType.ITALICS),
            TextNode("Bold Header", TextType.BOLD),
            TextNode("[image](www.google.com)", TextType.IMAGE),
        ]

        self.assertEqual(new_nodes, expected_new_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and this [other link](https://www.google.com)"
        )

        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("other link", "https://www.google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a [link](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a [link](https://google.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and an ![image](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_links([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and an ![image](https://google.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_2(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode(
            "[link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode(
            "There is no link",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("There is no link", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_no_image(self):
        node = TextNode(
            "There is no image",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("There is no image", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result_nodes = text_to_textnodes(text)

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALICS),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]

        self.assertListEqual(expected_nodes, result_nodes)

if __name__ == "__main__":
    unittest.main()
