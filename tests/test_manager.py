import os
import unittest
from db.manager import Manager
from db.models import *
from db.create import create_database, delete_database

class TestManager(unittest.TestCase):

    def setUp(self):
        self.cleanup = True
        create_database("mining.db")
        self.manager = Manager("mining.db")

    def tearDown(self):
        if self.cleanup:
            self.manager.session.close_all()
            delete_database("mining.db")

    def test_bulk_insert(self):
        arr_d_val = [
                     {'text':'1'},
                     {'text':'2'},
                     {'text':'3'},
                     {'text':'4'},
                     {'text':'5'},
                     {'text':'6'},
                     {'text':'7'}
                    ]
        for dict_val in arr_d_val:
            self.manager.bulk_insert_simple(
                dict_val=dict_val,
                instance=Word,
                list_search=['text'])

        
