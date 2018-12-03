import sqlite3


class Position:
    def __init__(self, user_id, site, _id=None):
        from banner.mapper import BannerMapper, PositionMapper
        self.user_id = user_id
        self.site = site
        self.banners = []
        connection = sqlite3.connect('db/sqlite.db')
        self.banner_mapper = BannerMapper(connection)
        self.position_mapper = PositionMapper(connection)
        self.id = _id

    def get_id(self):
        return self.id

    def get_hash(self):
        return hash(self.get_id)

    def assign_banner(self, banner):
        self.banner_mapper.assign(self, banner)

    def get_banners(self):
        self.banner_mapper.find_by_position(self)

    def deassign_banners(self, position, banner):
        pass

    def generate_widget_script(self):
        return '<script>let label = document.querySelectorAll("div[data-banner-label={}]");</script>'.format(self.get_hash())

    def generate_widget_label(self):
        return '<div data-banner-label="{}"></div>'.format(self.get_hash())

    def save(self):
        self.id = self.position_mapper.insert(self)
