import unittest
import train

class TestTrain(unittest.TestCase):

    def test_train(self):
        texts = [{u"Period": period,
                  u"Author": author,
                  u"Title": title,
                  u"URL": url}
                for author, title, period, url
                in train.parse_json("/home/johnny/berrynet/sources.json")]
        test_text = {
            u"Period": u"Romantic",
            u"Author": u"Percy Bysshe Shelley",
            u"Title": u"A Defence of Poetry and Other Essays",
            u"URL": u"http://www.gutenberg.org/cache/epub/5428/pg5428.txt"
        }
        for t in texts:
            print t
        self.assertIn(test_text, texts)
