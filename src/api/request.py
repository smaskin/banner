from user.model import User


class Request:
    TEST_SITE = 'https://google.com'
    TEST_USER = 'Test User Name'

    def __init__(self):
        self.reference = self.TEST_SITE
        self.region = Region.ALL
        self.user = User(self.TEST_USER)


class Region(object):
    ALL = '*'


