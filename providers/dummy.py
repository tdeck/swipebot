from provider import DataProvider
from time import time
from random import randint

class DummyProvider(DataProvider):
    def __init__(self):
        super(DummyProvider, self).__init__()
        self.name = 'dummy'

    def get_listing(self):
        print "get_listing()"
        return [
            (
                'abcd', 
                "Post one",
                "hash1",
                int(time()),
            ),
            (
                'efgh', 
                "Post two",
                "hash2",
                int(time()),
            ),
            (
                'ijkl', 
                "Post three",
                "hash3",
                int(time()),
            ),
            (
                'mnop', 
                "Post four",
                "hash4",
                int(time()),
            ),
        ]

    def get_rating(self, slug):
        print "get_rating(" + slug + ")"
        return (randint(0, 50), randint(0, 50))
