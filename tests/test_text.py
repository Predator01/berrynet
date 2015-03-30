# -*-coding:utf-8 -*-

import unittest
from core import train
import os
from core.settings import BASE_DIR

from .settings import TEST_TEXT_DIR

class TestTrain(unittest.TestCase):

    def setUp(self):
        path = os.path.join(BASE_DIR, 'sources.json')
        self.trainer = train.Trainer(json_path=path, text_dir=TEST_TEXT_DIR, db_url="test.db")

    def tearDown(self):
        pass

    def test_train(self):
        
        texts = [{"Period": period,
                  "Author": author,
                  "Title": title,
                  "URL": url}
                 for author, title, period, url
                 in self.trainer.json()
                ]
        test_text = {
            "Period": "Romantic",
            "Author": "Percy Bysshe Shelley",
            "Title": "A Defence of Poetry and Other Essays",
            "URL": "http://www.gutenberg.org/cache/epub/5428/pg5428.txt"
        }
        self.assertIn(test_text, texts)
