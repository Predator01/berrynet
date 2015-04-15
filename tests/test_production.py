# -*-coding:utf-8 -*-

import logging
from os import path
import unittest

from core.settings import BASE_DIR
from core.extract import Extractor
from core.train import Trainer
from core.query import Query

from db.create import create_database, delete_database
from db.models import Category, Period, Word, WordConditionalProbability

from core.extract import format_filename
from core.settings import BASE_DIR

from .settings import TEST_DIR
from .settings import TEST_TEXT_DIR


logger = logging.getLogger(__name__)


class TestQuery(unittest.TestCase):
    """
    This test allows for caching the database.
    """

    def setUp(self):
        self.db_url = path.join(BASE_DIR, "berrynet_trim.db")
        self.text_dir = path.join(BASE_DIR, "tests", "texts")

    def test_db_exists(self):
        self.assertTrue(path.isfile(self.db_url))

    # def test_simple_query(self):
    #     book_url = path.join(self.text_dir, "query-3.txt")
    #     self.assertTrue(path.isfile(book_url))
    #     with Query(self.text_dir, self.db_url, book_url, should_download=False) as query:
    #         e, r = query.results()
    #         # print c
    #         # print e, r
    #         self.assertTrue(e > r)

    def test_elizabethan_1(self):
        book_url = path.join(self.text_dir, "William Shakespeare-Romeo and Juliet.txt")
        self.assertTrue(path.isfile(book_url))
        with Query(self.text_dir, self.db_url, book_url, should_download=False) as query:
            e, r = query.results()
            print e, r
            logger.debug(e,r)
            self.assertTrue(e > r)

    # def test_elizabethan_1(self):
    #     book_url = path.join(path.join(TEST_DIR, "texts"), "query-2.txt")
    #     with Query(self.text_dir, self.db_url, book_url) as query:
    #         e, r = query.results()
    #         self.assertTrue(e > r)

    # def test_top(self):
    #     book_url = path.join(path.join(TEST_DIR, "texts"), "query-2.txt")
    #     with Query(self.text_dir, self.db_url, book_url) as query:
    #         t = query.top(2)
    #         print " top ------ "
    #         for u in t:
    #             print u

