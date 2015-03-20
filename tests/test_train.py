import unittest
import train

class TestTrain(unittest.TestCase):

    def test_train(self):
        texts = train.parse_json("/home/johnny/berrynet/sources.json")
        for author, title, period, url in texts:
            print author, title, period, url
