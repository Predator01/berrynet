import os
import unittest
import core.extract
import core.settings

class TestText(unittest.TestCase):

    def setUp(self):
        self.url = "http://www.gutenberg.org/cache/epub/7768/pg7768.txt"
        self.author = "Charles Lamb"
        self.title = "The Adventures of Ulysses"
        self.period = "Romantic"
        self.filename = "Charles Lamb-The Adventures of Ulysses.txt"
        self.file_fullname = os.path.join(core.extract.TEXTS_FOLDER, self.filename)

    def test_get_text_without_query(self):
        core.extract.get_text(self.url, query=False, author=self.author, title=self.title, period=self.period)
        self.assertTrue(os.path.isfile(self.file_fullname))

    def test_get_text_without_query(self):
        core.extract.get_text(self.url, query=False, author=self.author, title=self.title, period=self.period)
        print self.file_fullname
        self.assertTrue(os.path.isfile(self.file_fullname))

    def test_read_text(self):
        for k, v  in core.extract.read_text(self.file_fullname).items():
            print k, v
