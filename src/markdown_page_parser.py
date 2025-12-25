from htmlnode import LeafNode, ParentNode
from markdown_block_parser import BlockType, block_to_block_type, markdown_to_blocks
from markdown_inline_parser import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

import re

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown) 

  children_nodes = []
  
  for block in blocks:
    block_type = block_to_block_type(block)

    nodes = []
    match block_type:
      case BlockType.CODE:
        lines = block.split('\n')

        code_node = TextNode(f'{"\n".join(lines[1:-1])}\n', TextType.CODE_TEXT)

        children_nodes.append(ParentNode('pre', [text_node_to_html_node(code_node)]))
        continue
      case BlockType.HEADING:
        match = re.match(r"^(#{1,6}) (.*)", block)

        if match is None:
          raise Exception("Heading has incorrect syntax")

        nodes = text_to_children_nodes(match.group(2))
        tag = f'h{len(match.group(1))}'
      case BlockType.PARAGRAPH:
        nodes = text_to_children_nodes(block.replace('\n', ' '))
        tag = 'p'
      case BlockType.QUOTE:
        lines = block.split('\n')

        quote = lines[0][2:]
        for i in range(1, len(lines)):
          quote += lines[i][1:]

        nodes = text_to_children_nodes(quote)
        tag = 'blockquote'
      case BlockType.UNORDERED_LIST:
        lines = block.split('\n')

        for line in lines:
          nodes.append(ParentNode('li', text_to_children_nodes(line[2:])))
        tag = 'ul'
      case BlockType.ORDERED_LIST:
        lines = block.split('\n')

        for line in lines:
          nodes.append(ParentNode('li', text_to_children_nodes(line.split(".")[1][1:])))

        tag = 'ol'

    children_nodes.append(ParentNode(tag, nodes))

  return ParentNode('div', children_nodes)

def text_to_children_nodes(text):
  text_nodes = text_to_textnodes(text)
  return text_nodes_to_html_nodes(text_nodes)

def text_nodes_to_html_nodes(text_nodes):
  html_nodes = []

  for text_node in text_nodes:
    node = text_node_to_html_node(text_node)
    html_nodes.append(node)

  return html_nodes
