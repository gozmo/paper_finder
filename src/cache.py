from collections import defaultdict

class Cache:
    def __init__(self):
        self.__cache = defaultdict(dict)

    def set(self, key, papers):
        self.__cache[key] = papers

    def get(self, key):
        return self.__cache[key]

cache = Cache()
