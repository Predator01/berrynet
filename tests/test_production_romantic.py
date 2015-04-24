# -*-coding:utf-8 -*-

import json
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



db_url = path.join(BASE_DIR, "berrynet-2.db")
text_dir = path.join(BASE_DIR, "tests", "texts")
training_text_dir = path.join(BASE_DIR, "texts")
json_path = path.join(BASE_DIR, "sources.json")


def test_db_exists():
    assert path.isfile(db_url), db_url


def test_sources():
    assert path.isfile(json_path), json_path


def get_text_paths():
    with open(json_path, "r") as f:
        texts = json.load(f)
        for text in texts:
            author = text["Author"]
            title = text["Title"]
            period = text["Period"]
            url = text["URL"]
            filename = format_filename(author, title)
            yield filename, period
    

def test_training_set():
    """
    Queries based on each of the books in the training set.
    """
    for filename, period in get_text_paths():
        assert period in ("Elizabethan", "Romantic")
        if period == "Romantic":
        	yield _test_book, filename, period


def _test_book(filename, period):
    filepath = path.join(training_text_dir, filename)
    assert path.isfile(filepath), filepath
    with Query(text_dir, db_url, filepath, should_download=False) as q:
        e, r = q.results()
        if period == "Elizabethan":
            assert e > r, filename
        else:
            assert r > e, filename

