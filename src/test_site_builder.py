import unittest

from site_builder import SiteBuilder


class TestPageGenertor(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n\nsome text\n\nmore text"
        exptected = "Title"
        actual = SiteBuilder().extract_title(markdown)
        self.assertEqual(exptected, actual)

    def test_extract_title__not_first(self):
        markdown = "some text\n\nmore text\n\n# Title\n\nsome text\n\nmore text"
        exptected = "Title"
        actual = SiteBuilder().extract_title(markdown)
        self.assertEqual(exptected, actual)

    def test_extract_title__missing(self):
        markdown = "some text\n\nmore text\n\nNo Title\n\nsome text\n\nmore text"
        sb = SiteBuilder()
        self.assertRaises(Exception, sb.extract_title, markdown)
