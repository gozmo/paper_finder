class Cache:
    def __init__(self):
        self.__cache = dict()

    def set(self, key, papers):
        self.__cache[key] = papers

    def remove(self, key, paper_id):
        self.__cache[key] = [paper for paper in self.__cache[key] if paper_id != paper["id"]]

    def get(self, key):
        return self.__cache[key]

    def reset(self, key):
        self.__cache[key] = []

    def is_empty(self, key):
        return key not in self.__cache or len(self.__cache[key]) == 0

cache = Cache()
