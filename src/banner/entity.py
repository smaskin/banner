import abc

from api.request import Request
from banner.state import Status
from stats.storage import Statistic


class Banner(metaclass=abc.ABCMeta):
    TYPE_IMAGE = 1
    TYPE_HTML = 2

    def __init__(self, user, campaign, dto):
        self.id = None
        self.user = user
        self.campaign = campaign
        self.regions = dto.regions
        self.period = dto.period
        self.limiter = dto.limiter

        self.click_count = 0
        self.show_count = 0
        self.status = Status(self, dto.allowed)

    @abc.abstractmethod
    def get_json_fields(self):
        pass

    @abc.abstractmethod
    def get_data(self):
        pass

    @classmethod
    def create(cls, user, campaign, dto):
        if dto.content:
            return BannerHtml(user, campaign, dto)
        elif dto.image_url:
            return BannerImage(user, campaign, dto)
        else:
            raise TypeError('Banner type is not correct')

    def get_id(self):
        return self.id

    def is_active(self):
        return self.status.is_active()

    def click(self):
        self.click_count = self.click_count + 1

    def show(self):
        self.show_count = self.show_count + 1

    def get_show_count(self, raw=False):
        s = Statistic()
        return s.get_show_count(self.get_id()) if raw else self.show_count

    def get_click_count(self, raw=False):
        s = Statistic()
        return s.get_click_count(self.get_id()) if raw else self.click_count

    def get_json(self):
        common_json = {'id': self.get_id()}
        return {**common_json, **self.get_json_fields()}


class BannerHtml(Banner):
    def __init__(self, user, campaign, dto):
        super().__init__(user, campaign, dto)
        self.content = dto.content

    def get_json_fields(self):
        return {'content': self.content}

    def get_data(self):
        return self.content


class BannerImage(Banner):
    def __init__(self, user, campaign, dto):
        super().__init__(user, campaign, dto)
        self.image_url = dto.image_url

    def get_json_fields(self):
        return {'image_url': self.image_url}

    def get_data(self):
        return self.image_url


class Period:
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish

    def get_in(self, time):
        return self.start < time < self.finish


class Limiter:
    def __init__(self, show, click):
        self.show = show
        self.click = click

    def get_in(self, show_count, click_count):
        return self.in_show_limit(show_count) and self.in_click_limit(click_count)

    def in_show_limit(self, show_count):
        return self.show == 0 or show_count < self.show

    def in_click_limit(self, click_count):
        return self.click == 0 or click_count < self.click


class Regions:
    DELIMITER = ';'

    def __init__(self, names=None):
        self.names = names if names else ['*']

    def __str__(self):
        return self.DELIMITER.join(self.names)

    def match(self):
        request = Request()
        current = request.region
        return current in self.names
