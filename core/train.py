# -*- coding: utf-8 -*-

import extract
import json
import os
from settings import BASE_DIR
from os import listdir
from os.path import isfile, join
from extract import *
from db.manager import *
from db import models
import operator

import logging
logger = logging.getLogger(__name__)

class Trainer:

    def json(self, filename):
        if not hasattr(self, "_json"):
            _json = []
            texts = {}
            with open(filename, "r") as f:
                texts = json.load(f)
            for text in texts:
                author = text["Author"]
                title = text["Title"]
                period = text["Period"]
                url = text["URL"]
                _json.append((author, title, period, url))
        return _json

    def get_books(self, filename):
        """
        Gets the book if it is not in the texts folder otherwise dowload it
        """
        files = [ f for f in listdir(TEXTS_FOLDER) if isfile(join(TEXTS_FOLDER,f)) ]
        for author, title, period, url in self.json(filename):
            try:
                if not format_filename(author, title) in files:
                    book = extract.get_text(url, False, author, title, period)
            except:
                #TODO : ERROR 403
                pass

    #TODO
    def inspect(self, filename):
        """
        Check if the file is just text or an html page (if html then delete)
        """
        pass


    def train(self, filename):
        self.get_books(filename)
        self.populate(filename)
        self.categories()



    def populate(self, filename):
        output = []
        for author, title, period, url in self.json(filename):
            #insert period
            dic_period = {'name':period}
            list_search = ['name']
            period_obj = get_or_insert(dict_val=dic_period,
                instance=models.Period, list_search=list_search)
            #insert book
            words = read_text(os.path.join(TEXTS_FOLDER, format_filename(author, title)))
            tota_words = reduce(operator.add, words.values())
            logger.debug(words)
            logger.debug("Total Words: %s", tota_words)
            dic_book = {'name':title,
                'author':author,
                'period':period_obj,
                'total_words':tota_words,
                'sentence_total':0}
            list_search = ['name','author','period']
            book_obj = get_or_insert(dict_val=dic_book,
                instance=models.Book,list_search=list_search)
            #Words
            filename = format_filename(author, title)
            
            if len(words) == 0:
                continue

            logger.debug("Period id : %s %s" % (period_obj.id,period_obj.name))
            logger.debug("Book id : %s %s %s" % (book_obj.id,book_obj.name,book_obj.author))
            insert_words(words,book_obj,tota_words)

    def categories(self):
        words_all = get({},Word,[],True)
        for word_obj in words_all:
            calculate_categories(word_obj=word_obj)

    def calculate_categories(self, word_obj=None):
        if not word_obj:
            return False
        max_rate, min_rate = get_max_min_rate(word_obj)
        logger.debug("%f %f " % (max_rate, min_rate))