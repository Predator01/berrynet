# -*-coding:utf-8 -*-


import sys
import pycurl
import sqlalchemy


TEXTS_FOLDER = 'texts/'
DEFAULT_TEXT = 'default.txt'
EXTRA_CHARS = '",./\'-_?¿*:()[]{}¡!%$=0987654321“”‘’'


index = 1

def train():
    pass


def set_data_text():
    pass


def flush_query(words):
    global index
    for word, value in sorted(words.iteritems()):
        print index, word, value
        index += 1
    print '----------------------------------------------------------------'


def get_text(url, query=True, author="Unknown", title="Unknown", period="Unknown"):
    file_name = DEFAULT_TEXT if query else '_'.join([author, title]) + '.txt'
    with open(TEXTS_FOLDER + file_name, 'wb') as text_file:
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, text_file)
        curl.perform()
        curl.close()
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
                #flush_query(words)
                #words = {}
                limit = 500
            
            limit -= 1
            line = text_file.readline()

        flush_query(words)



if __name__ == '__main__':
    file_name = get_text(sys.argv[1], False)
    read_text(file_name)
