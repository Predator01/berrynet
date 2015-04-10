# -*- coding: utf-8 -*-

from __future__ import division

import json
import logging
import operator
import os
from os import listdir, mkdir
from os.path import isdir, isfile, join

import extract

from sqlalchemy import func 
from sqlalchemy import and_

from db import models

from .settings import BASE_DIR, TEXT_DIR

from extract import Extractor
from extract import format_filename
from db.manager import Manager

from db.models import Word
from db.models import *
from db.models import WordConditionalProbability

logger = logging.getLogger(__name__)


class Trainer(object):

    def __init__(self, json_path, text_dir, db_url):
        self.json_path = json_path
        self.text_dir = text_dir
        self.db_url = db_url
        if not isdir(self.text_dir):
            mkdir(self.text_dir)
        self.extractor = Extractor(text_dir)
        self.manager = Manager(db_url)

    def json(self):
        if not hasattr(self, "_json"):
            _json = []
            texts = {}
            with open(self.json_path, "r") as f:
                texts = json.load(f)
            for text in texts:
                author = text["Author"]
                title = text["Title"]
                period = text["Period"]
                url = text["URL"]
                _json.append((author, title, period, url))
        return _json

    def get_books(self):
        """
        Downloads the book if it's not in the texts directory.
        """
        files = [f for f in listdir(self.text_dir)]
        for author, title, period, url in self.json():
            filename = format_filename(author, title)
            if not filename in files:
                print filename
                book = self.extractor.download_book(url, False, author, title, period)

    def train(self):
        logger.debug("      STARTING get_books")
        self.get_books()
        logger.debug("      STARTING populate")
        self.populate()
        logger.debug("      STARTING categories")
        self.categories()
        logger.debug("      STARTING conditional_probability")
        self.conditional_probability()
        self.manager.session.close_all()    

    def populate(self):
        output = []
        for author, title, period, url in self.json():
            # TODO clean the next line
            words = self.extractor.read_text(format_filename(author, title))
            if len(words) == 0:
                continue
            total_words = reduce(operator.add, words.values())
            #insert period
            dic_period = {'name':period}
            list_search = ['name']
            period_obj = self.manager.get_or_insert(dict_val=dic_period,
                instance=models.Period, list_search=list_search)
            #insert book
            # logger.debug(words)
            logger.debug("Total Words: %s", total_words)
            dic_book = {'name':title,
                'author':author,
                'period':period_obj,
                'total_words':total_words,
                'sentence_total':0}
            list_search = ['name','author','period']
            book_obj = self.manager.get_or_insert(dict_val=dic_book,
                instance=models.Book,list_search=list_search)
            #Words
            filename = format_filename(author, title)
            
            if len(words) == 0:
                continue

            logger.debug("Period id : %s %s" % (period_obj.id,period_obj.name))
            logger.debug("Book id : %s %s %s" % (book_obj.id,book_obj.name,book_obj.author))
            self.manager.insert_words(words,book_obj,total_words)

    def categories(self):
        words_all = self.manager.get({},Word,[],True)
        total = len(words_all)
        logger.debug("  categories Words %s" % total)
        for word_obj in words_all:
            self.calculate_categories(word_obj=word_obj)
            total -= 1
            if total % 500 ==0:
                logger.debug("Progressing Word -- Category... %s" % total)
        self.manager.session.commit()

    def calculate_categories(self, word_obj=None):
        if not word_obj:
            return False
        max_rate, min_rate = self.manager.get_max_min_rate(word_obj)
        self.manager.construct_categories(min_rate,max_rate, word_obj)


    def period_probability(self, period, log=False):
        """
        # libros de esa epoca
        ---
        # total de libros
        """
        books_period = self.manager.session.query(Book).filter_by(period=period).count()
        if log:
            logger.debug("      books_period = %f " % (books_period))
        return books_period


    def word_category_period_probability(self, word, category, period, log=False):
        """
        cuenta cuantos (libros de esa epoca) tienen esa palabra en esa categoria
        ---
        numero de libros de esa epoca
        """
        num_books__word_cat = 0
        books_period = self.manager.session.query(Book).filter_by(period=period).all()
        for book in books_period:
            #el libro contiene la palabra
            book_word = self.manager.session.query(WordCount).filter_by(
                book=book,word=word).all()
            word_category = self.manager.session.query(WordCategory).filter_by(
                category=category,word=word).one()
            
            #if len(book_word)==0, no relation then prob 0 
            if len(book_word) > 0 and word_category:
                if book_word[0].rate >= word_category.min_range and book_word[0].rate < word_category.max_range:
                    num_books__word_cat += 1
        if log:
            logger.debug("      num_books__word_cat= %f" % (num_books__word_cat))

        return num_books__word_cat

    def probability(self, word, category, period, log=False):
        """
        probabilidad esa palabra en esa categoria en esa epoca
        ---
        probabilidad de esa epoca = # libros de esa epoca / cantidad de libros
        """
        word_category_period_probability = self.word_category_period_probability(word, category, period, log=log)
        period_probability = self.period_probability(period, log=log)
        if log:
            logger.debug("  word cat period prob = %f / period prob = %f = %f" % (word_category_period_probability,period_probability,word_category_period_probability/period_probability))
        return word_category_period_probability/period_probability


    def conditional_probability(self):
        """
        """
        self.manager.session.query(WordConditionalProbability).delete()
        bulk = []
        words_all = self.manager.session.query(Word).all()
        periods = self.manager.session.query(Period).all()
        categories = self.manager.session.query(Category).all()
        for period in periods:
            logger.debug(period.name)
            for category in categories:
                logger.debug(category.description)
                total = len(words_all)
                for word in words_all:
                    #word rate?
                    prob = self.probability(
                        word=word,
                        category=category,
                        period=period)
                    if prob > 1:
                        logger.debug("word %s category %s  period %s prob %s" % (word.text,category.description, period.name, prob))
                        self.probability(word=word,category=category,period=period, log=True)
                    word_cond_prob = WordConditionalProbability(
                        word=word,
                        category=category,
                        period=period,
                        probability=prob)
                    bulk.append(word_cond_prob)
                    total -= 1
                    if total % 500 == 0:
                        logger.debug("left ... %s words" % total)
        self.manager.session.add_all(bulk)
        self.manager.session.commit()
        self.complete_probability()

    def complete_probability(self):
        bulk = []
        list_cat = ['med','high','high_high']
        cats_ids = self.manager.session.query(Category).filter(Category.description.in_(list_cat)).all()
        low = self.manager.session.query(Category).filter(Category.description=='low').one()

        words_all = self.manager.session.query(Word).all()
        periods = self.manager.session.query(Period).all()
        for period in periods:
            total = len(words_all)
            for word in words_all:
                sum_3cat = self.manager.session.query(
                    func.sum(WordConditionalProbability.probability)).filter(
                        and_(WordConditionalProbability.id_category.in_(c.id for c in cats_ids),
                            WordConditionalProbability.id_word == word.id,
                            WordConditionalProbability.id_period == period.id)
                    ).all()[0][0]
                cat_low = self.manager.session.query(WordConditionalProbability).filter(
                        and_(WordConditionalProbability.id_category == low.id,
                            WordConditionalProbability.id_word == word.id,
                            WordConditionalProbability.id_period == period.id)
                    ).all()
                cat_low[0].probability = 1 - sum_3cat
                # print "word_id %s period %d sum %s" %(word.id,period.id,sum_3cat)
                total -= 1
                if total % 500 == 0:
                    logger.debug("left ... %s words" % total)
        self.manager.session.commit()

