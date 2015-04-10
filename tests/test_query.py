# -*-coding:utf-8 -*-

from os import path
import unittest

from core.settings import BASE_DIR
from core.extract import Extractor
from core.train import Trainer
from core.query import Query

from db.create import create_database, delete_database
from db.models import Category, Period, Word, WordConditionalProbability

from core.extract import format_filename

from .settings import TEST_DIR
from .settings import TEST_TEXT_DIR

import textfixtures

class TestQuery(unittest.TestCase):
    """
    This test allows for caching the database.
    """

    def setUp(self):
        self.cleanup = False
        json_path = path.join(TEST_DIR, "test-1.json")
        self.db_url = path.join(path.join(TEST_DIR, "db"), "test-2.db")
        textfixtures.bootstrap()
        self.trainer = Trainer(text_dir=TEST_TEXT_DIR, json_path=json_path, db_url=self.db_url)
        if not path.isfile(self.db_url):
            create_database(self.db_url)
            self.trainer.train()
        self.text_dir = path.join(TEST_DIR, "texts")
        self.db_url = path.join(path.join(TEST_DIR, "db"), "test-2.db")
        

    def tearDown(self):
        if self.cleanup:
            delete_database(self.db_url)

    def test_db_exists(self):
        self.assertTrue(path.isfile(self.db_url))

    def test_romantic_1(self):
        book_url = path.join(path.join(TEST_DIR, "texts"), "query-1.txt")
        with Query(self.text_dir, self.db_url, book_url) as query:
            e, r = query.results()
            self.assertTrue(r > e)

    def test_elizabethan_1(self):
        book_url = path.join(path.join(TEST_DIR, "texts"), "query-2.txt")
        with Query(self.text_dir, self.db_url, book_url) as query:
            e, r = query.results()
            self.assertTrue(e > r)
