import abc

from stats.stats import Statistic


class Banner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_json_fields(self):
        pass

    def __init__(self, user_id, data, campaign_id):
        self.user_id = user_id
        self.data = data
        self.campaign_id = campaign_id

    def get_id(self):
        return id(self)

    def get_json(self):
        common_json = {'id': self.get_id()}
        return {**common_json, **self.get_json_fields()}

    def get_show_count(self):
        s = Statistic()
        s.get_show_count(self.get_id())

    def get_click_count(self):
        s = Statistic()
        s.get_click_count(self.get_id())

    def save(self):
        pass


class BannerHtml(Banner):
    def get_json_fields(self):
        return {'content': self.data}


class BannerImage(Banner):
    def get_json_fields(self):
        return {'image_url': self.data}


class BannerFactory:
    TYPE_IMAGE = 1
    TYPE_HTML = 2

    def create(self, user_id, t, data, campaign_id) -> Banner:
        if t == self.TYPE_HTML:
            return BannerHtml(user_id, data, campaign_id)
        elif t == self.TYPE_IMAGE:
            return BannerImage(user_id, data, campaign_id)
        else:
            raise ValueError('Banner type is not correct')


