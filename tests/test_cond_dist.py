# -*-coding:utf-8 -*-

import os
import unittest

from core.settings import BASE_DIR
from core.extract import Extractor
from core.train import Trainer

from db.create import create_database, delete_database
from db.models import Category, Period, Word, WordConditionalProbability

from core.extract import format_filename

from .settings import TEST_DIR
from .settings import TEST_TEXT_DIR
import textfixtures


class TestConditionalProbability(unittest.TestCase):

    def setUp(self):
        self.cleanup = True
        json_path = os.path.join(TEST_DIR, "test-1.json")
        self.db_url = os.path.join(TEST_DIR, "test-1.db")
        textfixtures.bootstrap()
        self.trainer = Trainer(text_dir=TEST_TEXT_DIR, json_path=json_path, db_url=self.db_url)
        if not os.path.isfile(self.db_url):
            create_database(self.db_url)
            self.trainer.train()

    def tearDown(self):
        if self.cleanup:
            delete_database(self.db_url)

    def _word_conditional_probability(self, word, category, period):
        p = self.trainer.manager.session.query(WordConditionalProbability)
        p = p.join(Word).join(Period).join(Category)
        p = p.filter(Word.text == word, Category.description == category, Period.name == period)
        p = p.one()
        return p.probability

    def test_A_low_given_R(self):
        p = self._word_conditional_probability('a', 'low', 'Romantic')
        self.assertAlmostEqual(0.4, p)

    def test_B_med_given_E(self):
        p = self._word_conditional_probability('b', 'med', 'Elizabethan')
        self.assertAlmostEqual(0.4, p)

    def test_C_high_given_R(self):
        p = self._word_conditional_probability('c', 'high', 'Romantic')
        self.assertAlmostEqual(0.6, p)

    def test_C_high_given_E(self):
        p = self._word_conditional_probability('c', 'high', 'Elizabethan')
        self.assertAlmostEqual(0.0, p)
