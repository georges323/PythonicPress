import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multi_children_type(self):
        node = ParentNode(
            "div", 
            [
                LeafNode("p", "heading"),
                ParentNode("div", 
                [
                    ParentNode("span", 
                   [
                        LeafNode(None, "key: "),
                        LeafNode(None, "value")
                    ])
                ]),
                LeafNode("p", "footer")
            ])

        self.assertEqual(node.to_html(), "<div><p>heading</p><div><span>key: value</span></div><p>footer</p></div>")

    def test_multi_children_type_and_props(self):
        node = ParentNode(
            "div", 
            [
                LeafNode("p", "heading"),
                ParentNode("div", 
                [
                    ParentNode("span", 
                   [
                        LeafNode(None, "key: "),
                        LeafNode(None, "value")
                    ],
                               { 'class': 'd-flex align-item-center', 'primary': 'blue'})
                ]),
                LeafNode("p", "footer")
            ],
            { 'class': 'd-flex justify-content-between'})

        self.assertEqual(node.to_html(), '<div class="d-flex justify-content-between"><p>heading</p><div><span class="d-flex align-item-center" primary="blue">key: value</span></div><p>footer</p></div>')

if __name__ == "__main__":
    unittest.main()
