# -*-coding:utf-8 -*-

import sys

from core.extract import get_text, read_text

if __name__ == '__main__':
    file_name = get_text(sys.argv[1], False)
    read_text(file_name)
