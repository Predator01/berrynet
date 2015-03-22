import os
import unittest
import db.manager.bulk_insert

class TestManager(unittest.TestCase):

    def test_bulk_insert():
        arr_d_val = [
        {'text':'1'},
        {'text':'2'},
        {'text':'3'},
        {'text':'4'},
        {'text':'5'},
        {'text':'6'},
        {'text':'7'},]
        bulk_insert( 
            arr_dict_val=arr_d_val,
            instance=Word
            )

        
