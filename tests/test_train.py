# -*-coding:utf-8 -*-

import unittest
from core import train
import os
import core.settings

class TestTrain(unittest.TestCase):

    def test_train(self):
        path = os.path.join(core.settings.BASE_DIR, 'sources.json')
        texts = [{"Period": period,
                  "Author": author,
                  "Title": title,
                  "URL": url}
                 for author, title, period, url
                 in train.json(path)[0:3]
                ]
        test_text = {
            "Period": "Romantic",
            "Author": "Percy Bysshe Shelley",
            "Title": "A Defence of Poetry and Other Essays",
            "URL": "http://www.gutenberg.org/cache/epub/5428/pg5428.txt"
        }
        for t in texts:
            print t
        self.assertIn(test_text, texts)
