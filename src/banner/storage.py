import sqlite3
import time
from banner.mapper import PositionMapper


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Repository(metaclass=Singleton):
    TYPE_POSITION = 1
    TIMEOUT_FOR_TEST = .1

    def __init__(self):
        connection = sqlite3.connect('db/sqlite.db')
        self.position_mapper = PositionMapper(connection)

    def get_banners_by_position_hash(self, _hash):
        time.sleep(self.TIMEOUT_FOR_TEST)
        return self.get_position_by_hash(_hash).get_banners()

    def get_position_by_hash(self, _hash):
        return self.position_mapper.get(_hash)


class Cache(metaclass=Singleton):
    def __init__(self):
        self.storage = {}

    def get_or_set(self, key, func):
        cached = self.storage.get(key)
        if not cached:
            loaded = func()
            self.storage.update({key: loaded})
            return loaded
        return cached

    def invalidate(self, key):
        self.storage.pop(key, None)
