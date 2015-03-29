import os
import unittest
from db.manager import *
from db.models import *

class TestManager(unittest.TestCase):

    def test_bulk_insert(self):
        arr_d_val = [
        {'text':'1'},
        {'text':'2'},
        {'text':'3'},
        {'text':'4'},
        {'text':'5'},
        {'text':'6'},
        {'text':'7'},]
        for dic_val in arr_d_val:
            bulk_insert_simple(
                dict_val=dic_val,
                instance=Word,
                list_search=['text']
                )

        
