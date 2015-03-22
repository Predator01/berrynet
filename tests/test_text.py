import os
import unittest
import core.extract
import core.settings

class TestText(unittest.TestCase):

    def setUp(self):
        self.url = "http://www.gutenberg.org/cache/epub/7256/pg7256.txt"
        self.author = "O. Henry"
        self.title = "The Gift of the Magi"
        self.period = "Unknown"
        self.filename = "O. Henry-The Gift of the Magi.txt"
        self.file_fullname = os.path.join(core.extract.TEXTS_FOLDER, self.filename)
        self.created = False

    def tearDown(self):
        if self.created:
            os.remove(self.file_fullname)

    def test_get_text_without_query(self):
        core.extract.get_text(self.url, query=False, author=self.author, title=self.title, period=self.period)
        self.assertTrue(os.path.isfile(self.file_fullname))
        self.created = True

    def test_get_text_without_query(self):
        core.extract.get_text(self.url, query=False, author=self.author, title=self.title, period=self.period)
        print self.file_fullname
        self.assertTrue(os.path.isfile(self.file_fullname))
        self.created = True

    def test_read_text(self):
        core.extract.get_text(self.url, query=False, author=self.author, title=self.title, period=self.period)
        for k, v  in core.extract.read_text(self.file_fullname).items():
            print k, v
