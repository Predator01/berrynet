# -*-coding:utf-8 -*-
import os
from core.settings import BASE_DIR

import sys
from os.path import isfile, join
from core.extract import get_text, read_text
from db.create import create_database

from core.train import Trainer


if __name__ == '__main__':
	
	create_database()
	filename = os.path.join(BASE_DIR, "sources.json")
	Trainer().train(filename)

    # file_name = get_text(sys.argv[1], False)
    # read_text(file_name)
