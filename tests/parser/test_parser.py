import unittest
from parser.parser import parse_string, parse_inline

"""
Tests for weave.parser.parser
"""

class TestParseString(unittest.TestCase):

    # -------------------------------------------------------------------------
    # Headings
    # -------------------------------------------------------------------------

    def test_h1(self):
        self.assertEqual(parse_string("# Heading"), "<h1>Heading</h1>\n")

    def test_h2(self):
        self.assertEqual(parse_string("## Heading"), "<h2>Heading</h2>\n")

    def test_h3(self):
        self.assertEqual(parse_string("### Heading"), "<h3>Heading</h3>\n")

    def test_h4(self):
        self.assertEqual(parse_string("#### Heading"), "<h4>Heading</h4>\n")

    def test_h5(self):
        self.assertEqual(parse_string("##### Heading"), "<h5>Heading</h5>\n")

    def test_h6(self):
        self.assertEqual(parse_string("###### Heading"), "<h6>Heading</h6>\n")

    def test_heading_capped_at_h6(self):
        self.assertEqual(parse_string("####### Heading"), "<h6>Heading</h6>\n")

    def test_heading_strips_leading_space(self):
        self.assertEqual(parse_string("#  Heading"), "<h1>Heading</h1>\n")

    # -------------------------------------------------------------------------
    # Paragraphs
    # -------------------------------------------------------------------------

    def test_paragraph(self):
        self.assertEqual(parse_string("Hello world"), "<p>Hello world</p>\n")

    def test_multiple_paragraphs(self):
        input_md = "First paragraph\n\nSecond paragraph"
        expected = "<p>First paragraph</p>\n<p>Second paragraph</p>\n"
        self.assertEqual(parse_string(input_md), expected)

    def test_empty_lines_ignored(self):
        input_md = "\n\n\nHello\n\n\n"
        self.assertEqual(parse_string(input_md), "<p>Hello</p>\n")

    # -------------------------------------------------------------------------
    # Lists
    # -------------------------------------------------------------------------

    def test_single_list_item(self):
        self.assertEqual(parse_string("- Item"), "<ul>\n    <li>Item</li>\n</ul>\n")

    def test_multiple_list_items(self):
        input_md = "- Item 1\n- Item 2\n- Item 3"
        expected = "<ul>\n    <li>Item 1</li>\n    <li>Item 2</li>\n    <li>Item 3</li>\n</ul>\n"
        self.assertEqual(parse_string(input_md), expected)

    def test_list_closes_before_paragraph(self):
        input_md = "- Item 1\n- Item 2\n\nParagraph"
        expected = "<ul>\n    <li>Item 1</li>\n    <li>Item 2</li>\n</ul>\n<p>Paragraph</p>\n"
        self.assertEqual(parse_string(input_md), expected)

    def test_list_closes_before_heading(self):
        input_md = "- Item 1\n## Heading"
        expected = "<ul>\n    <li>Item 1</li>\n</ul>\n<h2>Heading</h2>\n"
        self.assertEqual(parse_string(input_md), expected)

    def test_list_at_end_of_file_closes(self):
        input_md = "# Heading\n\n- Item 1\n- Item 2"
        expected = "<h1>Heading</h1>\n<ul>\n    <li>Item 1</li>\n    <li>Item 2</li>\n</ul>\n"
        self.assertEqual(parse_string(input_md), expected)

    # -------------------------------------------------------------------------
    # Blockquotes
    # -------------------------------------------------------------------------

    def test_blockquote(self):
        self.assertEqual(parse_string("> Quote"), "<blockquote>Quote</blockquote>\n")

    def test_blockquote_closes_list(self):
        input_md = "- Item\n> Quote"
        expected = "<ul>\n    <li>Item</li>\n</ul>\n<blockquote>Quote</blockquote>\n"
        self.assertEqual(parse_string(input_md), expected)

    # -------------------------------------------------------------------------
    # Horizontal rules
    # -------------------------------------------------------------------------

    def test_horizontal_rule(self):
        self.assertEqual(parse_string("***"), "<hr />\n")

    def test_horizontal_rule_many_stars(self):
        self.assertEqual(parse_string("*****"), "<hr />\n")

    def test_horizontal_rule_closes_list(self):
        input_md = "- Item\n***"
        expected = "<ul>\n    <li>Item</li>\n</ul>\n<hr />\n"
        self.assertEqual(parse_string(input_md), expected)

    # -------------------------------------------------------------------------
    # Inline code
    # -------------------------------------------------------------------------

    def test_inline_code(self):
        self.assertEqual(parse_string("`code`"), "<p><code>code</code></p>\n")

    def test_inline_code_closes_list(self):
        input_md = "- Item\n`code`"
        expected = "<ul>\n    <li>Item</li>\n</ul>\n<p><code>code</code></p>\n"
        self.assertEqual(parse_string(input_md), expected)

    # -------------------------------------------------------------------------
    # Mixed content
    # -------------------------------------------------------------------------

    def test_heading_then_paragraph(self):
        input_md = "# Heading\n\nThis is a paragraph."
        expected = "<h1>Heading</h1>\n<p>This is a paragraph.</p>\n"
        self.assertEqual(parse_string(input_md), expected)

    def test_heading_list_paragraph(self):
        input_md = "# Heading\n\n- Item 1\n- Item 2\n\nThis is a paragraph."
        expected = "<h1>Heading</h1>\n<ul>\n    <li>Item 1</li>\n    <li>Item 2</li>\n</ul>\n<p>This is a paragraph.</p>\n"
        self.assertEqual(parse_string(input_md), expected)

    def test_empty_string(self):
        self.assertEqual(parse_string(""), "")

    def test_only_empty_lines(self):
        self.assertEqual(parse_string("\n\n\n"), "")


class TestParseInline(unittest.TestCase):

    # -------------------------------------------------------------------------
    # Bold
    # -------------------------------------------------------------------------

    def test_bold(self):
        self.assertEqual(parse_inline("**bold**"), "<strong>bold</strong>")

    def test_bold_in_sentence(self):
        self.assertEqual(parse_inline("this is **bold** text"), "this is <strong>bold</strong> text")

    # -------------------------------------------------------------------------
    # Italic
    # -------------------------------------------------------------------------

    def test_italic(self):
        self.assertEqual(parse_inline("*italic*"), "<em>italic</em>")

    def test_italic_in_sentence(self):
        self.assertEqual(parse_inline("this is *italic* text"), "this is <em>italic</em> text")

    # -------------------------------------------------------------------------
    # Bold + italic
    # -------------------------------------------------------------------------

    def test_bold_italic(self):
        self.assertEqual(parse_inline("***bold italic***"), "<strong><em>bold italic</em></strong>")

    def test_bold_italic_in_sentence(self):
        self.assertEqual(parse_inline("this is ***bold italic*** text"), "this is <strong><em>bold italic</em></strong> text")

    # -------------------------------------------------------------------------
    # Plain text
    # -------------------------------------------------------------------------

    def test_plain_text(self):
        self.assertEqual(parse_inline("no formatting here"), "no formatting here")

    def test_empty_string(self):
        self.assertEqual(parse_inline(""), "")


if __name__ == "__main__":
    unittest.main()
