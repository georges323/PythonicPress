from enum import Enum

from htmlnode import LeafNode, ParentNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALICS = 'italic'
    CODE_TEXT = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type is None:
        raise ValueError("Text Node has no text type")
            
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALICS:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None or text_node.url == '':
                raise ValueError("Link Text Node has an empty url")

            return LeafNode("a", text_node.text, { 'href': text_node.url })
        case TextType.IMAGE:
            if text_node.url is None or text_node.url == '':
                raise ValueError("Image Text Node has an empty url")

            if text_node.text is None or text_node.text == '':
                raise ValueError("Image Text Node has an empty alt text")

            return LeafNode("img", "", { 'src': text_node.url, 'alt': text_node.text })
        case _:
            raise Exception('Text Node text type does not exist')


