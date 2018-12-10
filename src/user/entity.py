import random


class User:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.default_region = '*'

    def set_id(self, _id):
        self.id = _id

    def get_id(self):
        return self.id


class Campaign:
    def __init__(self, user, name=None):
        self.id = None
        self.user = user
        self.name = name if name else 'Default campaign for {}'.format(user.name)

    def set_id(self, _id):
        self.id = _id

    def get_id(self):
        return 0 if self.name.startswith('Default campaign') else self.id


class Position:
    def __init__(self, user, site, _hash=None):
        self.id = None
        self.user = user
        self.site = site
        self.hash = _hash if _hash else hash(random.random())

    def set_id(self, _id):
        self.id = _id

    def get_id(self):
        return self.id

    def generate_widget_script(self):
        return '<script>let label = document.querySelectorAll("div[data-banner-label={}]");</script>'.format(self.hash)

    def generate_widget_label(self):
        return '<div data-banner-label="{}"></div>'.format(self.hash)
