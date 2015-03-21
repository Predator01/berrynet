# -*- coding: utf-8 -*-

import json

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
