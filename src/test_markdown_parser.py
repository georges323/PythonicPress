import unittest

from htmlnode import ParentNode, LeafNode
from markdown_parser import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType

class TestMarkdownParser(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
