import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_props_to_html(self):
    props = {
      'href': 'https://www.google.com',
      'target': '_blank'
    }

    node = HTMLNode("p", "hello", props=props)

    self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

  def test_props_to_html_none(self):
    node = HTMLNode("p", "hello")

    self.assertEqual(node.props_to_html(), '')

  def test_values(self):
    node = HTMLNode("span", "testing")

    self.assertEqual(node.tag, "span")
    self.assertEqual(node.value, "testing")
    self.assertEqual(node.children, None)
    self.assertEqual(node.props, None)
  
  def test_repr(self):
    node = HTMLNode("div", "another test", None, {'class': 'div-1'})

    self.assertEqual(node.__repr__(), "HTMLNode(div, another test, children: None, {'class': 'div-1'})")


if __name__ == "__main__":
  unittest.main()
