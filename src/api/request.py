from user.entity import User


class Request:
    TEST_SITE = 'https://google.com'
    TEST_USER = 'Test User Name'

    def __init__(self):
        self.reference = self.TEST_SITE
        self.region = Region.ALL
        self.user = User(self.TEST_USER)
        self.server_post = {}

    def post(self, attribute=None):
        return self.server_post[attribute] if attribute in self.server_post else self.server_post


class Region(object):
    ALL = '*'


