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

def parse_json(filename):
    texts = {}
    with open(filename, "r") as f:
        texts = json.load(f)
    for text in texts:
        author = text["Author"]
        title = text["Title"]
        period = text["Period"]
        url = text["URL"]
        yield author, title, period, url

def get_books(filename):
    files = [ f for f in listdir(TEXTS_FOLDER) if isfile(join(TEXTS_FOLDER,f)) ]
    for author, title, period, url in parse_json(filename):
        #TODO : ERROR 403
        try:
            book = extract.get_text(url, False, author, title, period, files)
        except:
            pass

#TODO
def inspect(filename):
    """
    Check if the file is just text or an html page (if html then delete)
    """
    pass


def train(filename):
    # get_books(filename)
    populate(filename)

def populate(filename):

    for author, title, period, url in parse_json(filename):
        #insert period
        dic_period = {'name':period}
        list_search = ['name']
        period_obj = get_or_insert(dict_val=dic_period,
            instance=models.Period, list_search=list_search)
        print "Period id : %s " % period_obj.id
        #insert book
        dic_book = {'name':title,
            'author':author,
            'period':period_obj,
            'total_words':0,
            'sentence_total':0}
        list_search = ['name','author','period']
        book_obj = get_or_insert(dict_val=dic_book,
            instance=models.Book,list_search=list_search)
        print "Book id : %s " % book_obj.id
        #Words
        filename = format_filename(author, title)
        words = read_text(filename)
        if len(words) == 0:
            continue
        insert_words(words,book_obj)
        

if __name__ == "__main__":
    filename = os.path.join(BASE_DIR, "sources.json")
    train(filename)

