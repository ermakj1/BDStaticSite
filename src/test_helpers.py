from helpers import *
from blocks import *
import unittest

class TestHelpers(unittest.TestCase):
    def test_plain_text(self):
        input = "This is a plain text"
        node = TextNode(input, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes[0], node)

    def test_bold_all(self):
        input = "*This is all bold*"
        node = TextNode(input, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This is all bold", TextType.BOLD))

    def test_bold_partial(self):
        input = "This is *partially* bold"
        node = TextNode(input, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("partially", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" bold", TextType.TEXT))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_link(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and link [link](www.internet.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and link [link](www.internet.com)"
        )
        self.assertListEqual([("link", "www.internet.com")], matches)

    def test_split_images_noop(self):
        node = TextNode("hello world", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)

    def test_split_link_noop(self):
        node = TextNode("hello world", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([node], new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![first image](https://i.imgur.com/firstimage.png) and another ![second image](https://i.imgur.com/secondimage.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("first image", TextType.IMAGE, "https://i.imgur.com/firstimage.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/secondimage.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/image.png) and another [link](https://i.imgur.com/link.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/image.png) and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/link.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_with_endlines_to_textnodes(self):
        #text with newlines should be treated as a single text node
        input = "This is line 1\nThis is line 2\nThis is line3"
        nodes = text_to_textnodes(input)

        #check to make sure there is only one node and it is a text node with the correct value
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[0].text, input)




if __name__ == "__main__":
    unittest.main()
