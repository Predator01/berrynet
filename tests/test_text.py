import os
import unittest
import core.extract
import core.settings

class TestText(unittest.TestCase):

    def test_get_text_without_query(self):
        author = "Charles Lamb"
        title = "The Adventures of Ulysses"
        period = "Romantic"
        core.extract.get_text("http://www.gutenberg.org/cache/epub/7768/pg7768.txt",
            query=False, author=author, title=title, period=period)
        filename = "Charles Lamb-The Adventures of Ulysses.txt"
        filename = os.path.join(os.path.join(core.settings.BASE_DIR, "texts"), filename)
        self.assertTrue(os.path.isfile(filename))

    def test_get_text_without_query(self):
        author = "Charles Lamb"
        title = "The Adventures of Ulysses"
        period = "Romantic"
        core.extract.get_text("http://www.gutenberg.org/cache/epub/7768/pg7768.txt",
            query=False, author=author, title=title, period=period)
        filename = "Charles Lamb-The Adventures of Ulysses.txt"
        filename = os.path.join(os.path.join(core.settings.BASE_DIR, "texts"), filename)
        self.assertTrue(os.path.isfile(filename))

    def test_read_text(self):
        pass
