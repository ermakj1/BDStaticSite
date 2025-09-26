import unittest

from textnode import TextNode, TextType
from website import extract_title


class TestWebsite(unittest.TestCase):
    def test_header(self):
        markdown = "# This is the Title"
        title = extract_title(markdown)
        self.assertEqual(title, "This is the Title")
    
    def test_no_header(self):
        markdown = "This is some content without a header."
        with self.assertRaises(ValueError) as context:
            title = extract_title(markdown)
            print(f"Title: {title}")
        self.assertEqual(str(context.exception), "No title found in markdown content")

    def test_header_but_h2(self):
        markdown = "## This is not the title"
        with self.assertRaises(ValueError) as context:
            title = extract_title(markdown)
            print(f"Title: {title}")
        self.assertEqual(str(context.exception), "No title found in markdown content")
    


if __name__ == "__main__":
    unittest.main()