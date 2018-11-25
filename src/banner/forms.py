import abc
import datetime

from api.request import Request
from user.campaign import Campaign


class Range(object):
    def __init__(self, start=None, finish=None):
        self.start = start if start else datetime.datetime.now()
        self.finish = finish if finish else datetime.datetime.now() + datetime.timedelta(weeks=4)


class Limiter(object):
    def __init__(self, show, click):
        self.start = show
        self.finish = click


class Form(metaclass=abc.ABCMeta):
    TYPE_IMAGE = 1
    TYPE_HTML = 2

    def __init__(self, fields):
        request = Request()
        user = request.user
        self.campaign = Campaign(user, fields['campaign']) if 'campaign' in fields else user.default_campaign
        self.regions = fields['regions'] if 'regions' in fields else []
        self.range = Range(fields['start'], fields['finish']) if 'start' in fields and 'finish' in fields else Range()
        self.limiter = Limiter(fields['show'] if 'show' in fields else 0, fields['click'] if 'click' in fields else 0)
        self.allowed = fields['allowed'] if 'allowed' in fields else True
        self.data = fields['content'] or fields['image_url'] or ''

    @abc.abstractmethod
    def get_json_fields(self):
        pass

    @classmethod
    def create(cls, t, fields):
        if t == cls.TYPE_HTML:
            return HtmlForm(fields)
        elif t == cls.TYPE_IMAGE:
            return ImageForm(fields)
        else:
            raise TypeError('Banner type is not correct')


class HtmlForm(Form):
    def get_json_fields(self):
        return {'content': self.data}


class ImageForm(Form):
    def get_json_fields(self):
        return {'image_url': self.data}
