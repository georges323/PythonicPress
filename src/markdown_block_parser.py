from enum import Enum
import re

class BlockType(Enum):
  PARAGRAPH = 'paragraph'
  HEADING = 'heading'
  CODE = 'code'
  QUOTE = 'quote'
  UNORDERED_LIST = 'unordered_list'
  ORDERED_LIST = 'ordered_list'

def extract_title(markdown):
    blocks = markdown.split("\n\n")

    if len(blocks) < 2 and not blocks[0].startswith('# '):
        raise ValueError('There needs to be an `h1` header at the start of the page!')

    return blocks[0].split('# ')[1]

def markdown_to_blocks(markdown):
  blocks= markdown.split("\n\n")

  return list(filter(lambda block: len(block) > 0, map(lambda block: block.strip(), blocks)))

def block_to_block_type(block):
  if is_heading(block):
    return BlockType.HEADING
  elif is_code_block(block):
    return BlockType.CODE
  elif is_quote_block(block):
    return BlockType.QUOTE
  elif is_unordered_list(block):
    return BlockType.UNORDERED_LIST
  elif is_ordered_list(block):
    return BlockType.ORDERED_LIST
  else:
    return BlockType.PARAGRAPH

def is_heading(block):
  return re.search(r"^#{1,6} ", block) is not None

def is_code_block(block):
  lines = block.split('\n')
  
  return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")

def is_quote_block(block):
  lines = block.split('\n')

  for line in lines:
    if not line.startswith('>'):
      return False

  return True

def is_unordered_list(block):
  lines = block.split('\n')

  for line in lines:
    if not line.startswith('- '):
      return False

  return True

def is_ordered_list(block):
  lines = block.split('\n')

  for i in range(0, len(lines)):
    match = re.match(r"^(\d+). ", lines[i])
    
    if match is None:
      return False
    
    number = int(match.group(1))
    if number != i + 1:
      return False
    

  return True

