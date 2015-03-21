# -*-coding:utf-8 -*-

import sys
import urllib2
import sqlalchemy

TEXTS_FOLDER = 'texts/'
DEFAULT_TEXT = 'default.txt'
EXTRA_CHARS = '",./\'-_?¿*:()[]{}¡!%$=0987654321“”‘’'


def train():
    pass


def set_data_text():
    pass


def flush_query(words):
    pass


def get_text(url, query=True, author="Unknown", title="Unknown", period="Unknown"):
    file_name = DEFAULT_TEXT if query else '_'.join([author, title]) + '.txt'
    with open(TEXTS_FOLDER + file_name, 'wb') as text_file:
        response = urllib2.urlopen(url)
        text = response.read()
        text_file.write(text)
    return file_name


def read_text(file_name):
    words = {}
    sentences = {}

    with open(TEXTS_FOLDER + file_name, 'r') as text_file:
        line = text_file.readline()
        limit = 500
        
        while line:
            line = line.split()

            for word in line:
                word = word.strip(EXTRA_CHARS)
                word = word.lower()
                words[word] = words[word] + 1 if words.has_key(word) else 1
            
            if limit == 0:
                flush_query(words)
                words = {}
                limit = 500
            
            limit -= 1
            line = text_file.readline()

        flush_query(words)
