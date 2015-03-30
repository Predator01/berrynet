# -*- coding: utf-8 -*-

from __future__ import division
from create import *
from models import *
from db.create import create_session
from sqlalchemy import func 
import logging

session = create_session()

logger = logging.getLogger(__name__)

def insert(dict_val, instance=None, list_search=None):
    if not instance:
        return instance
    temp = instance(**dict_val)
    session.add(temp)
    return get(dict_val,instance,list_search)

def get(dict_val, instance=None, list_search=None, get_all=False):
    if not instance:
        return instance
    if get_all:
        return session.query(instance).all()
    dic_search = {}
    for k,v in dict_val.items():
        if k in list_search:
            dic_search[k] = v
    try:
        item = session.query(instance).filter_by(**dic_search).all()[0]
    except IndexError:
        item = None
    return item


def get_or_insert(dict_val, instance=None, list_search=None):
    if not instance:
        return instance

    item = get(dict_val, instance, list_search)
    if not item:
        item = insert(dict_val, instance, list_search)
        session.commit()
    return item

# def bulk_insert(arr_dict_val, instance):
#     if not instance:
#         return False
#     for params in arr_dict_val:
#         temp = instance(**params)
#         # if not exist(temp):
#             # session.add(temp)
#     session.commit()
#     return True

def bulk_insert_simple(dict_val, instance=None, list_search=None):
    if not instance:
        return instance
    item = get(dict_val, instance, list_search)
    if not item:
        item = instance(**dict_val)
    return item


def insert_words(dic_words, book_obj=None, total_words=0):
    if not book_obj:
        return book_obj
    objs = []

    logger.debug("## loading words for book %s" % book_obj.name)
    total = len(dic_words)
    for word, num in dic_words.items():
        try:
            word = unicode(word)
            total-=1
            #TODO Too much time processing
            # word_obj = get_or_insert(
            #     dict_val={'text':word},
            #     instance=Word,
            #     list_search=['text'])
            word_obj = bulk_insert_simple(
                dict_val={'text':word},
                instance=Word,
                list_search=['text'])
            word_count_obj = bulk_insert_simple(
                dict_val={'book':book_obj, 'word':word_obj,
                'count':num, 'rate':num/total_words},
                instance=WordCount,
                list_search=['book','word'])
            objs.append(word_obj)
            objs.append(word_count_obj)
        except:
            logger.debug("Parsing error: %s" % word)
        if total % 500 ==0:
            logger.debug("Progressing ... %s" % total)
    session.add_all(objs)
    session.commit()
    return True


def get_max_min_rate(word=None):
    if not word:
        return None,None
    float_word_max = session.query(func.max(WordCount.rate)).filter_by(word=word).all()
    float_word_min = session.query(func.min(WordCount.rate)).filter_by(word=word).all()
    float_word_max = float_word_max[0][0]
    float_word_min = float_word_min[0][0]
    if float_word_max == float_word_min:
        float_word_min = 0
    return float_word_max, float_word_min


def construct_categories(min_rate, max_rate, word_obj=None):
    if not word_obj:
        return word_obj
    #load categories
    list_dic_cat = [{'description':'low'},{'description':'med'},{'description':'high'},{'description':'high_high'}]
    list_search = ['description']
    offset = (max_rate - min_rate) / len(list_dic_cat)
    min_cat_rate = 0
    objs = []
    for dic_category in list_dic_cat:
        category_obj = bulk_insert_simple(
            dict_val=dic_category,
            instance=Category,
            list_search=list_search)
        word_category_obj = bulk_insert_simple(
            dict_val={'category':category_obj, 'word':word_obj,
            'min_range': min_cat_rate, 'max_range': min_cat_rate+offset },
            instance=WordCategory,
            list_search=['category','word'])
        min_cat_rate += offset
        objs.append(word_category_obj)
        objs.append(category_obj)
    session.add_all(objs)
