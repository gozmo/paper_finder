from collections import defaultdict
from src import io_utils

class Cache:
    def set(self, key, papers):
        io_utils.cache_write(key, papers)

    def get(self, key):
        return io_utils.cache_read(key)

cache = Cache()
