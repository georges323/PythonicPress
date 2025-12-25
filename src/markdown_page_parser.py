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

    if block_type == BlockType.PARAGRAPH:
      block = block.replace('\n', ' ')
      text_nodes = text_to_textnodes(block)
      html_nodes = text_nodes_to_html_nodes(text_nodes)
      children_nodes.append(ParentNode('p', html_nodes))
      continue

    if block_type == BlockType.HEADING:
      match = re.match(r"^(#{1,6}) (.*)", block)

      if match is None:
        raise Exception("Heading has incorrect syntax")

      heading_number = len(match.group(1)) # so the space after the # is not included
      children_nodes.append(LeafNode(f'h{heading_number}', match.group(2)))
      continue

    if block_type == BlockType.CODE:
      lines = block.split('\n')

      code_node = TextNode(f'{"\n".join(lines[1:-1])}\n', TextType.CODE_TEXT)
      children_nodes.append(ParentNode('pre', [text_node_to_html_node(code_node)]))
      continue

    if block_type == BlockType.QUOTE:
      lines = block.split('\n')

      quote = lines[0][2:]
      for i in range(1, len(lines)):
        quote += lines[i][1:]
      
      text_nodes = text_to_textnodes(quote)
      children_nodes.append(ParentNode('blockquote', text_nodes_to_html_nodes(text_nodes)))

      continue

    if block_type == BlockType.UNORDERED_LIST:
      lines = block.split('\n')

      unordered_list = []
      for line in lines:
        text_nodes = text_to_textnodes(line[2:])
        unordered_list.append(ParentNode('li', text_nodes_to_html_nodes(text_nodes)))

      children_nodes.append(ParentNode('ul', unordered_list))
      continue

    if block_type == BlockType.ORDERED_LIST:
      lines = block.split('\n')

      ordered_list = []
      for line in lines:
        text_nodes = text_to_textnodes(line.split(".")[1][1:])
        ordered_list.append(ParentNode('li', text_nodes_to_html_nodes(text_nodes)))

      children_nodes.append(ParentNode('ol', ordered_list))

  return ParentNode('div', children_nodes)

def text_nodes_to_html_nodes(text_nodes):
  html_nodes = []

  for text_node in text_nodes:
    node = text_node_to_html_node(text_node)
    html_nodes.append(node)

  return html_nodes
