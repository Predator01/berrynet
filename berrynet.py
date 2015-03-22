# -*-coding:utf-8 -*-

import sys

from core.extract import get_text, read_text
from db.create import create_database

if __name__ == '__main__':
    create_database()
    file_name = get_text(sys.argv[1], False)
    read_text(file_name)
