# -*-coding:utf-8 -*-
import os
from core.settings import BASE_DIR

import sys
from os.path import isfile, join
from core.extract import get_text, read_text
from db.create import create_database

from core.train import Trainer


if __name__ == '__main__':
    json_path = os.path.join(BASE_DIR, "sources.json")
    db_url = os.path.join(BASE_DIR, "berrynet.db")
    test_dir = os.path.join(BASE_DIR, "/texts")
    trainer = Trainer(text_dir=test_dir, json_path=json_path, db_url=db_url)
    if not os.path.isfile(db_url):
        create_database(db_url)
        trainer.train()
