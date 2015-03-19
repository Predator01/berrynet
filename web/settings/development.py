# -*- encoding:utf-8 -*-

import os

from common import *

DEBUG = True

DEBUG_TB_PANELS = [
    'flask_mongoengine.panels.MongoDebugPanel'
]

SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
FLASK_ROOT = os.path.dirname(SETTINGS_DIR)
PROJECT_ROOT = os.path.dirname(FLASK_ROOT)

DB_NAME = 'cancan.db'
DB_REPOSITORY = 'db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, DB_NAME)
SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_ROOT, DB_REPOSITORY)
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = True