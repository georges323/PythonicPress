from htmlnode import LeafNode, ParentNode
from markdown_block_parser import BlockType, block_to_block_type, markdown_to_blocks
from markdown_inline_parser import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

import re

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown) 

  children_nodes = []
  
  for block in blocks:
    block_html_node = block_to_html_node(block)
    children_nodes.append(block_html_node)

  return ParentNode('div', children_nodes)

def block_to_html_node(block):
  block_type = block_to_block_type(block)
  match block_type:
    case BlockType.CODE:
      return code_block_to_html_node(block)
    case BlockType.HEADING:
      return heading_block_to_html_node(block)
    case BlockType.PARAGRAPH:
      return paragraph_block_to_html_node(block)
    case BlockType.QUOTE:
      return quote_block_to_html_node(block)
    case BlockType.UNORDERED_LIST:
      return unordered_list_to_html_node(block)
    case BlockType.ORDERED_LIST:
      return ordered_list_to_html_node(block)

def code_block_to_html_node(block):
  lines = block.split('\n')

  code_text_node = TextNode(f'{"\n".join(lines[1:-1])}\n', TextType.CODE_TEXT)
  child_node = text_node_to_html_node(code_text_node)

  return ParentNode('pre', [child_node])

def heading_block_to_html_node(block):
  match = re.match(r"^(#{1,6}) (.*)", block)

  if match is None:
    raise Exception("Heading has incorrect syntax")

  return ParentNode(f'h{len(match.group(1))}', text_to_children_nodes(match.group(2)))

def paragraph_block_to_html_node(block):
  children = text_to_children_nodes(block.replace('\n', ' '))
  return ParentNode('p', children)

def quote_block_to_html_node(block):
  lines = block.split('\n')

  quote = lines[0][2:]
  for i in range(1, len(lines)):
    quote += lines[i][1:]

  return ParentNode('blockquote', text_to_children_nodes(quote))

def unordered_list_to_html_node(block):
  lines = block.split('\n')

  children= []
  for line in lines:
    children.append(ParentNode('li', text_to_children_nodes(line[2:])))

  return ParentNode('ul', children)

def ordered_list_to_html_node(block):
  lines = block.split('\n')

  children= []
  for line in lines:
    children.append(ParentNode('li', text_to_children_nodes(line.split(".")[1][1:])))

  return ParentNode('ol', children)

def text_to_children_nodes(text):
  text_nodes = text_to_textnodes(text)
  return text_nodes_to_html_nodes(text_nodes)

def text_nodes_to_html_nodes(text_nodes):
  html_nodes = []

  for text_node in text_nodes:
    node = text_node_to_html_node(text_node)
    html_nodes.append(node)

  return html_nodes
