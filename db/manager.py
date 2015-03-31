# -*- coding: utf-8 -*-

from __future__ import division

import logging

from sqlalchemy import func 

from .models import *
from .create import create_session

logger = logging.getLogger(__name__)


class Manager(object):

    def __init__(self, url):
        self.session = create_session(url)      

    def insert(self, dict_val, instance=None, list_search=None):
        if not instance:
            return instance
        temp = instance(**dict_val)
        self.session.add(temp)
        return self.get(dict_val,instance,list_search)


    #TODO Refactor
    def get(self, dict_val, instance=None, list_search=None, get_all=False):
        if not instance:
            return instance
        if get_all and not list_search:
            return self.session.query(instance).all()
        dic_search = {}
        for k,v in dict_val.items():
            if k in list_search:
                dic_search[k] = v
        try:
            if get_all:
                item = self.session.query(instance).filter_by(**dic_search).all()
            else:
                item = self.session.query(instance).filter_by(**dic_search).all()[0]
        except IndexError:
            item = None
        return item


    def get_or_insert(self, dict_val, instance=None, list_search=None):
        if not instance:
            return instance

        item = self.get(dict_val, instance, list_search)
        if not item:
            item = self.insert(dict_val, instance, list_search)
            self.session.commit()
        return item

    def bulk_insert_simple(self, dict_val, instance=None, list_search=None):
        if not instance:
            return instance
        item = self.get(dict_val, instance, list_search)
        if not item:
            item = instance(**dict_val)
        return item


    def insert_words(self, dic_words, book_obj=None, total_words=0):
        if not book_obj:
            return book_obj
        objs = []

        logger.debug("## loading words for book %s" % book_obj.name)
        total = len(dic_words)
        for word, num in dic_words.items():
            try:
                word = unicode(word)
                total-=1
                word_obj = self.bulk_insert_simple(
                    dict_val={'text':word},
                    instance=Word,
                    list_search=['text'])
                word_count_obj = self.bulk_insert_simple(
                    dict_val={'book':book_obj, 'word':word_obj,
                    'count':num, 'rate':num/total_words},
                    instance=WordCount,
                    list_search=['book','word'])
                objs.append(word_obj)
                objs.append(word_count_obj)
            except Exception, e:
                logger.debug("Parsing error: %s <Error>%s</Error>" % (word,e))
            if total % 500 ==0:
                logger.debug("Progressing ... %s" % total)
        self.session.add_all(objs)
        self.session.commit()
        return True


    def get_max_min_rate(self, word=None):
        if not word:
            return None,None
        float_word_max = self.session.query(func.max(WordCount.rate)).filter_by(word=word).all()[0][0]
        float_word_min = self.session.query(func.min(WordCount.rate)).filter_by(word=word).all()[0][0]
        return float_word_max, float_word_min


    def construct_categories(self, min_rate, max_rate, word_obj=None):
        if not word_obj:
            return word_obj
        #load categories
        list_dic_cat = [{'description':'low'},{'description':'med'},{'description':'high'},{'description':'high_high'}]
        list_search = ['description']

        offset = (max_rate - min_rate) / len(list_dic_cat)
        #min_rate == max_rate
        if offset == 0:
            offset = max_rate / len(list_dic_cat)
        
        min_cat_rate = min_rate
        objs = []
        #TODO Refatorizar
        #min
        low = list_dic_cat[0]
        category_obj = self.bulk_insert_simple(
            dict_val=low,
            instance=Category,
            list_search=list_search)
        word_category_obj = self.bulk_insert_simple(
            dict_val={'category':category_obj, 'word':word_obj,
            'min_range': 0, 'max_range': min_rate},
            instance=WordCategory,
            list_search=['category','word'])
        objs.append(word_category_obj)
        objs.append(category_obj)   
        #intermedias
        for dic_category in list_dic_cat[1:-1]:
            category_obj = self.bulk_insert_simple(
                dict_val=dic_category,
                instance=Category,
                list_search=list_search)
            word_category_obj = self.bulk_insert_simple(
                dict_val={'category':category_obj, 'word':word_obj,
                'min_range': min_cat_rate, 'max_range': min_cat_rate+offset },
                instance=WordCategory,
                list_search=['category','word'])
            min_cat_rate += offset
            objs.append(word_category_obj)
            objs.append(category_obj)
        #max
        high_high = list_dic_cat[-1]
        category_obj = self.bulk_insert_simple(
            dict_val=high_high,
            instance=Category,
            list_search=list_search)
        word_category_obj = self.bulk_insert_simple(
            dict_val={'category':category_obj, 'word':word_obj,
            'min_range': min_cat_rate, 'max_range': 1.0},
            instance=WordCategory,
            list_search=['category','word'])
        objs.append(word_category_obj)
        objs.append(category_obj)   
        
        self.session.add_all(objs)
