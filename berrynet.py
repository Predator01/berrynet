# -*-coding:utf-8 -*-

import os
import sys

from core.settings import BASE_DIR
from db.create import create_database
from core.train import Trainer


if __name__ == '__main__':
    try:
        json_path = os.path.join(BASE_DIR, "sources.json")
        db_url = os.path.join(BASE_DIR, "berrynet.db")
        test_dir = os.path.join(BASE_DIR, "texts")
        trainer = Trainer(text_dir=test_dir, json_path=json_path, db_url=db_url)
        if not os.path.isfile(db_url):
            create_database(db_url)
            trainer.train()
    except Exception as e:
        print type(e)
        print "=================="
        print e
        print "=================="
        for i in e:
            print i
            print "------------"
    print "Finished!"
