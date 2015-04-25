"""
Verifies that all texts in sources.json exist
"""

import os.path

from core import train
from core.settings import TEXT_DIR, BASE_DIR
from core.extract import format_filename

path = os.path.join(BASE_DIR, 'sources.json')
trainer = train.Trainer(json_path=path, text_dir=TEXT_DIR, db_url="")

def test_sources():
    for author, title, period, url in trainer.json():
        yield _test_exists, format_filename(author, title)

def _test_exists(filename):
    filepath = os.path.join(TEXT_DIR, filename)
    assert os.path.isfile(filepath), filename
