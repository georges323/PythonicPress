import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
  def test_p_tag_to_html(self):
    node = LeafNode("p", "Hello, world!")

    self.assertEqual(node.to_html(), '<p>Hello, world!</p>')

  def test_div_tag_with_props_to_html(self):
    node = LeafNode("p", "Hello, world!", { 'class': 'd-flex', 'primary': 'blue'})

    self.assertEqual(node.to_html(), '<p class="d-flex" primary="blue">Hello, world!</p>')

  def test_empty_value_none(self):
    node = LeafNode("p", None)

    with self.assertRaises(ValueError) as context:
            node.to_html()
    self.assertIn("All leaf nodes must have a value", str(context.exception))

  def test_values(self):
    node = LeafNode("span", "testing", { 'class': 'example' })

    self.assertEqual(node.tag, "span")
    self.assertEqual(node.value, "testing")
    self.assertEqual(node.children, None)
    self.assertEqual(node.props, { 'class': 'example' })
  
if __name__ == "__main__":
  unittest.main()
