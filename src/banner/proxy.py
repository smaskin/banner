import abc

from api.request import Request
from banner.storage import Repository, Cache


class BannerProxy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_banners_by_position_hash(self, _hash):
        pass


class AuthProxy(BannerProxy):
    def __init__(self) -> None:
        self.request = Request()
        self.cacheProxy = CachedProxy()

    def get_banners_by_position_hash(self, _hash):
        position = self.cacheProxy.get_position_by_hash(_hash)
        if self.request.reference != position.site:
            raise PermissionError()
        return self.cacheProxy.get_banners_by_position_hash(_hash)


class CachedProxy(BannerProxy):
    def __init__(self) -> None:
        self.repository = Repository()
        self.cache = Cache()

    def get_banners_by_position_hash(self, _hash):
        return self.cache.get_or_set('bs_{}'.format(_hash), lambda: self.repository.get_banners_by_position_hash(_hash))

    def get_position_by_hash(self, _hash):
        return self.cache.get_or_set('p_{}'.format(_hash), lambda: self.repository.get_position_by_hash(_hash))

    def invalidate_position_hash(self, position_hash):
        return self.cache.invalidate(position_hash)
