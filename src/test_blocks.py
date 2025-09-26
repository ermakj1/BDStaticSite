from helpers import *
from blocks import *
from htmlnode import *
import unittest

class BlockTestHelpers(unittest.TestCase):
    def test_plain_text(self):
        self.assertEqual(block_to_blocktype("This is a plain text paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("```\nThis is code\n```"), BlockType.CODE)
        self.assertEqual(block_to_blocktype("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype("- This is an unordered list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_blocktype("1. This is an ordered list item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype("```python\nprint('Hello, World!')\n```"), BlockType.CODE)
        self.assertEqual(block_to_blocktype("## a"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("### a"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("#### a"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("####a"), BlockType.PARAGRAPH)  # No space after # is not a heading
        self.assertEqual(block_to_blocktype("##### a"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("###### a"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("####### a"), BlockType.PARAGRAPH)  # More than 6 # is not a heading

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
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_header(self):
        md = "# H1 Header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>H1 Header</h1></div>")

        md = "## H2 Header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>H2 Header</h2></div>")

        md = "##### H5 Header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h5>H5 Header</h5></div>")

        md = "###### H6 Header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h6>H6 Header</h6></div>")

        md = "####### Not a Header " \
        "This should be a paragraph because there are 7 #"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>####### Not a Header This should be a paragraph because there are 7 #</p></div>")

    def test_unordered_list(self):
        md = """- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_ordered_list(self):
        md = """1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>") 
    
    def test_blockquote(self):
        md = """> This is a quote
> that spans multiple lines
> and should be included in the quote.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote that spans multiple lines and should be included in the quote.</blockquote></div>")
        

if __name__ == "__main__":
    unittest.main()
