import abc
import datetime
import sqlite3

from banner.state import PublishedStatus
from banner.mapper import BannerMapper, UserMapper
from stats.storage import Statistic


class Banner(metaclass=abc.ABCMeta):
    TYPE_IMAGE = 1
    TYPE_HTML = 2

    def __init__(self, user, data, campaign):
        connection = sqlite3.connect('db/sqlite.db')
        self.banner_mapper = BannerMapper(connection)
        if type(user) is int:
            user_mapper = UserMapper(connection)
            user = user_mapper.get(user)
        self.data = data
        self.campaign = campaign
        self.regions = [user.default_region]
        self.start = datetime.datetime.now()
        self.finish = datetime.datetime.now() + datetime.timedelta(weeks=1)
        self.allowed = True
        self.click_limit = 0
        self.show_limit = 0
        self.click_count = 0
        self.show_count = 0

        self.user = user
        self.status = PublishedStatus(self)
        self.id = None

    @abc.abstractmethod
    def get_json_fields(self):
        pass

    @classmethod
    def create(cls, user, t, data, campaign=None):
        if t == cls.TYPE_HTML:
            return BannerHtml(user, data, campaign)
        elif t == cls.TYPE_IMAGE:
            return BannerImage(user, data, campaign)
        else:
            raise TypeError('Banner type is not correct')

    def get_id(self):
        return self.id

    def change_status(self, status):
        self.status = status

    def is_active(self):
        return self.status.is_active()

    def click(self):
        self.click_count = self.click_count + 1
        self.status.click()

    def show(self):
        self.show_count = self.show_count + 1
        self.status.show()

    def get_show_count(self, raw=False):
        s = Statistic()
        return s.get_show_count(self.get_id()) if raw else self.show_count

    def get_click_count(self, raw=False):
        s = Statistic()
        return s.get_click_count(self.get_id()) if raw else self.click_count

    def get_json(self):
        common_json = {'id': self.get_id()}
        return {**common_json, **self.get_json_fields()}

    def save(self):
        self.id = self.banner_mapper.insert(self)


class BannerHtml(Banner):
    def get_json_fields(self):
        return {'content': self.data}


class BannerImage(Banner):
    def get_json_fields(self):
        return {'image_url': self.data}
