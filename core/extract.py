# -*-coding:utf-8 -*-

import os
import sys
import urllib2
import sqlalchemy
import settings


TEXTS_FOLDER = os.path.join(settings.BASE_DIR, "texts")
DEFAULT_FILENAME = 'default.txt'
EXTRA_CHARS = '",./\'-_?¿*;:()[]{}¡!%$=0987654321“”‘’'


def train():
    pass


def set_data_text():
    pass


def flush_query(words):
    pass

def format_filename(author="Unknown", title="Unknown"):
    return "%s-%s.txt" % (author, title)

def get_text(url, query=True, author="Unknown", 
    title="Unknown", period="Unknown"):
    """
    Gets the text from the url
    """
    filename = DEFAULT_FILENAME if query else format_filename(author, title)
    filename = os.path.join(TEXTS_FOLDER, filename)
    with open(filename, 'wb') as text_file:
        response = urllib2.urlopen(url)
        text = response.read()
        text_file.write(text)
    return filename


def prepare_line(line):
    """
    Splits a line into several words/
    """
    for word in line.split():
        word = word.strip(EXTRA_CHARS)
        word.lower()
        if word:
            yield word


def read_text(filename):
    """
    Receives the filename (no full path), returns a dictionary where the key
    is each word in the text and the value is the count of that word.
    """
    words = {}
    filename = os.path.join(TEXTS_FOLDER, filename)
    with open(filename, 'r') as text_file:
        for line in text_file:
            for word in prepare_line(line):
                words[word] = words.get(word, 0) + 1
    return words
