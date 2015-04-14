# -*-coding:utf-8 -*-

import itertools
import os
from os import mkdir
from os.path import isdir
import sys
import urllib2

import sqlalchemy

import settings

DEFAULT_FILENAME = 'default.txt'
EXTRA_CHARS = '",./\'-_?¿*;:()[]{}¡!%$=0987654321“”‘’'
INWORD_PUNCTUATION = ["--"]


def is_html(text):
    return "<head>" in text


def prepare_line(line):
    """
    Splits a line into several words.
    """
    words = line.split()
    words = map(lambda w: w.strip(EXTRA_CHARS), words)
    words = map(lambda w: w.lower(), words)
    for sep in INWORD_PUNCTUATION:
        words = map(lambda w: w.split(sep),words)
        words = list(itertools.chain.from_iterable(words))
    return words


def format_filename(author="Unknown", title="Unknown"):
    return "%s-%s.txt" % (author, title)


class Extractor(object):
    """
    By default works with the production directory of texts. It can be
    overridden for testing. Works with files in the said directory.
    """

    def __init__(self, text_dir):
        self.text_dir = text_dir if text_dir else settings.TEXT_DIR
        if not isdir(self.text_dir):
            mkdir(self.text_dir)

    def read_text(self, filename):
        """
        Receives the filename (no full path), returns a dictionary where the key
        is each word in the text and the value is the count of that word.
        """
        words = {}
        filename = os.path.join(self.text_dir, filename)
        with open(filename, 'r') as text_file:
            for line in text_file:
                for word in prepare_line(line):
                    words[word] = words.get(word, 0) + 1
        return words
    
    def download_book(self, url, query=False, author="Unknown", title="Unknown", period="Unknown"):
        """
        Downloads text from a URL. Returns the resulting filename if it was
        succesfully downloaded, otherwise returns None.
        """
        filename = DEFAULT_FILENAME if query else format_filename(author, title)
        filename = os.path.join(self.text_dir, filename)
        response = urllib2.urlopen(url)
        text = response.read()
        if is_html(text):
            return None
        with open(filename, 'wb') as text_file:
            text_file.write(text)
        return filename
