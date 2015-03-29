# -*- coding: utf-8 -*-

from create import *
from models import *
from db.create import create_session
session = create_session()

import logging
logger = logging.getLogger(__name__)

def insert(dict_val, instance=None, list_search=None):
    if not instance:
        return instance
    temp = instance(**dict_val)
    session.add(temp)
    return get(dict_val,instance,list_search)

def get(dict_val, instance=None, list_search=None):
    if not instance:
        return instance
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
        
        
def bulk_insert(arr_dict_val, instance):
    if not instance:
        return False
    for params in arr_dict_val:
        temp = instance(**params)
        if not exist(temp):
            session.add(temp)
    session.commit()
    return True

def bulk_insert_simple(dict_val, instance=None, list_search=None):
    if not instance:
        return instance
    item = get(dict_val, instance, list_search)
    if not item:
        item = instance(**dict_val)
    return item


def insert_words(dic_words, book_obj=None):
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
                dict_val={'book':book_obj, 'word':word_obj,'count':num},
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
