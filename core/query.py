# -*- coding: utf-8 -*-

import os
from os import path

from db.manager import Manager
from extract import DEFAULT_FILENAME
from extract import Extractor
from db.models import *


class Query(object):

    def __init__(self, text_dir, db_url, book_url, should_download=False):
        """
        ``text_dir`` is the directory where a copy of text should be put.
        ``db_url`` should be the url to a database that already exists.
        ``should_download`` indicates whether or not ``book_url`` is a local
        path or a url in the internet.
        """
        self.text_dir = text_dir
        self.db_url = db_url
        self.book_url = book_url
        self.should_download = should_download
        self.manager = Manager(db_url)
        self.extractor = Extractor(text_dir)

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, type, value, traceback):
        self.clean_up()

    def run(self):
        word_rates = self._word_rates()
        word_categories = self._word_categories(word_rates)
        wcp = self._word_conditional_probabilities(word_categories)
        e, r = self._probabilities(wcp)
        self.elizabethan_factor = e
        self.romantic_factor = r

    def results(self):
        """
        Returns a tuple (e, r) with the factor that this book be Elizabethan
        or Romantic respectively.
        """
        return self.elizabethan_factor, self.romantic_factor


    def clean_up(self):
        if self.should_download:
            os.remove(self.filename)
        
    def _word_rates(self):
        """
        Downloads the book if needed, or makes a copy of it.
        Returns a dictionary of words and their rates.
        """
        if self.should_download:
            self.filename = self.extractor.download_book(self.book_url, True)
        else:
            self.filename = self.book_url
        word_rates = self.extractor.read_text(self.filename)
        self.word_rates = word_rates
        return word_rates
        
    def _word_categories(self, word_rates):
        """
        For every word in the database returns a dictionary of word->category
        according to the rates in the books.
        Returns an iterable of WordCategory for the category of every word that
        is both in the book and the database, returns the WordCategory with
        lowest category for words in the database that did not appear in the
        book.
        """
        total_words = reduce(lambda x, y: x + y, word_rates.itervalues())
        rates = {w: (float(c) / total_words)
            for w, c in word_rates.iteritems()}
        for w, r in rates.iteritems():
            print "word = %s, rate = %f" % (w, r)
        words = self.manager.session.query(Word).all()
        low = self.manager.session.query(Category)
        low = low.filter(Category.description=='low').one()
        low_id = low.id
        for word in words:
            wc = self.manager.session.query(WordCategory)
            wc = wc.filter(WordCategory.id_word==word.id)
            rate = rates.get(word.text)
            if rate:
                wc = wc.filter(WordCategory.min_range <= rate)
                wc = wc.filter(WordCategory.max_range > rate)
            else:
                wc = wc.filter(WordCategory.id_category == low_id)
            print " word = %s" % word.text
            print " rate = %r" % rate
            wc = wc.one()
            yield wc
        
    def _word_conditional_probability(self, word_id, category_id, period_id):
        """
        Returns an instace of WordConditionalProbability.
        """
        p = self.manager.session.query(WordConditionalProbability)
        p = p.filter_by(id_word=word_id, id_category=category_id,
            id_period=period_id)
        p = p.one()
        return p
    
    def _word_conditional_probabilities(self, word_categories):
        """
        Receives an iterable of WordCategory objects.
        Yields a tuples of ``(e, r)`` where ``e`` and ``r`` are the
        probabilities that the word and category be in Elizabethan and Romantic
        periods respectively.
        """
        elizabethan = self.manager.elizabethan_period
        romantic = self.manager.romantic_period
        for wc in word_categories:
            word_id = wc.id_word
            category_id = wc.id_category
            e = self._word_conditional_probability(word_id, category_id,
                elizabethan.id).probability
            r = self._word_conditional_probability(word_id, category_id,
                romantic.id).probability
            yield e, r

    def _probabilities(self, conditional_probabilities):
        """
        Receives an iterable as returned by
        ``_word_conditional_probabilities``.
        
        Returns a tuple ``(e, r)`` of the factor than this book be Elizabethan
        or Romantic respectively.
        """
        elizabethan_book_count = self.manager.elizabethan_book_count
        romantic_book_count = self.manager.romantic_book_count
        total_books = elizabethan_book_count + romantic_book_count
        elizabethan_probability = float(elizabethan_book_count) / total_books
        romantic_probability = float(romantic_book_count) / total_books
        elizabethan_factor = 1
        romantic_factor = 1
        for e, r in conditional_probabilities:
            if e != 0 and r != 0:
                elizabethan_factor *= e * elizabethan_probability
                romantic_factor *= r * romantic_probability
            print "e = %f, r = %f" % (elizabethan_factor, romantic_factor)
        return elizabethan_factor, romantic_factor

    def top(self, count):
        ordered = sorted(self.word_rates.iteritems(), key=lambda x: -x[1])
        return ordered[0:count]

