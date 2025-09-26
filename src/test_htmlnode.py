from htmlnode import *
from textnode import *
import unittest

from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello", [], {"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})
    
    def test_props_to_html(self):
        node = HTMLNode("div", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')

    def test_repr(self):
        node = HTMLNode("div", "Hello", [], {"class": "my-class"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello, [], {'class': 'my-class'})")

    def test_leaf_node_val(self):
        leaf = LeafNode("img", "value of the image node", {"src": "image.png"})
        self.assertEqual(leaf.tag, "img")

    def test_leaf_node_no_val(self):
        with self.assertRaises(ValueError) as context:
            leaf = LeafNode("img", None, {"src": "image.png"})
        self.assertEqual(str(context.exception), "LeafNode must have a value")

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_with_endlines(self):
        node = TextNode("This is a text\nnode", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text\nnode")

    def test_nested(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        bold = TextNode("This is a bold node", TextType.BOLD)
        html_bold = text_node_to_html_node(bold)
        parent = ParentNode("div", [html_node, html_bold])        
        self.assertEqual(parent.to_html(), "<div>This is a text node<b>This is a bold node</b></div>")

if __name__ == "__main__":
    unittest.main()
