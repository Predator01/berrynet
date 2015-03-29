import unittest
from core import train
import os
import core.settings

class TestTrain(unittest.TestCase):

    def test_train(self):
        path = os.path.join(core.settings.BASE_DIR, 'sources.json')
        texts = [{u"Period": period,
                  u"Author": author,
                  u"Title": title,
                  u"URL": url}
                 for author, title, period, url
                 in train.Trainer().json(path)[0:3]
                ]
        test_text = {
            u"Period": u"Romantic",
            u"Author": u"Percy Bysshe Shelley",
            u"Title": u"A Defence of Poetry and Other Essays",
            u"URL": u"http://www.gutenberg.org/cache/epub/5428/pg5428.txt"
        }
        for t in texts:
            print t
        self.assertIn(test_text, texts)
