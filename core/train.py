# -*- coding: utf-8 -*-

import extract
import json
import os

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

def train(filename):
    for author, title, period, url in parse_json(filename):
        extract.get_text(url, False, author, title, period)


if __name__ == "__main__":
    filename = os.path.join(BASE_DIR, "sources.json")
    train(filename)
