import unittest

from markdown_block_parser import BlockType, block_to_block_type, is_code_block, is_heading, is_ordered_list, is_quote_block, is_unordered_list, markdown_to_blocks

class TestMarkdownBlockParser(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_is_heading(self):
      self.assertEqual(True, is_heading('### Heading 3'))

    def test_is_heading_syntax_fail(self):
      self.assertEqual(False, is_heading('###Heading 3'))

    def test_is_heading_number_of_pound(self):
      self.assertEqual(False, is_heading('####### Heading 7'))

    def test_is_code_block_empty(self):
      self.assertEqual(True, is_code_block('```\n```'))
    
    def test_is_code_block_multiline(self):
      code_block="``` var x = 10;\nconsole.log(x);\nconsole.log(x == 10);\n```"

      self.assertEqual(True, is_code_block(code_block))

    def test_is_code_block_syntax_fail(self):
      self.assertEqual(False, is_code_block('``` This is a code block ``'))

    def test_is_quote_block(self):
      self.assertEqual(True, is_quote_block('>Quote 1\n>Quote 2'))

    def test_is_quote_block_empty(self):
      self.assertEqual(True, is_quote_block('>\n>'))

    def test_is_quote_block_fail(self):
      self.assertEqual(False, is_quote_block('>Quote 1\nQuote 2'))

    def test_is_unordered_list(self):
      self.assertEqual(True, is_unordered_list('- unordered 1\n- unordered 2\n- unordered 3'))

    def test_is_unordered_list_empty(self):
      self.assertEqual(True, is_unordered_list('- '))

    def test_is_unordered_list_fail(self):
      self.assertEqual(False, is_unordered_list('- success\n-fail'))

    def test_is_ordered_list(self):
      self.assertEqual(True, is_ordered_list('1. one\n2. two\n3. three\n4. four'))

    def test_is_ordered_list_empty(self):
      self.assertEqual(True, is_ordered_list('1. '))

    def test_is_ordered_list_fail_on_order(self):
      self.assertEqual(False, is_ordered_list('1. one\n2. two\n4. three\n4. four'))

    def test_is_ordered_list_syntax_fail(self):
      self.assertEqual(False, is_ordered_list('1. one\n2.two\n3. three\n4. four'))

    def test_block_to_block_type_heading(self):
      self.assertEqual(BlockType.HEADING, block_to_block_type('###### Heading 6'))

    def test_block_to_block_type_code(self):
      self.assertEqual(BlockType.CODE, block_to_block_type('```\n   console.log("hello world");\n```'))

    def test_block_to_block_type_quote(self):
      self.assertEqual(BlockType.QUOTE, block_to_block_type("> quote 1\n> quote2"))

    def test_block_to_block_type_unordered_list(self):
      self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type('- one\n- two\n- three'))

    def test_block_to_block_type_ordered_list(self):
      self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type('1. one\n2. two\n3. three'))

    def test_block_to_block_type_paragraph(self):
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type('This is a paragraph 1. one 2. two'))

if __name__ == "__main__":
    unittest.main()
