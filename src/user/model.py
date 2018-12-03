import sqlite3

from user.campaign import Campaign
from user.position import Position


class User:
    def __init__(self, name):
        self.id = None
        from banner.mapper import UserMapper
        connection = sqlite3.connect('db/sqlite.db')
        self.user_mapper = UserMapper(connection)

        self.name = name
        self.default_campaign = Campaign(self, 'Default campaign for {}'.format(name))
        self.default_region = '*'

        self.banners = []
        self.positions = []
        self.campaigns = []

    def get_id(self):
        return self.id

    def create_banner(self, t, data, campaign_id=None):
        from banner.model import Banner
        banner = Banner.create(self, t, data, campaign_id if campaign_id else self.default_campaign)
        banner.save()
        self.banners.append(banner)

    def delete_banner(self, id):
        pass

    def create_position(self, site_name: str):
        position = Position(self.get_id(), site_name)
        position.save()
        self.positions.append(position)

    def delete_position(self, id):
        pass

    def create_campaign(self, name: str):
        campaign = Campaign(self, name)
        self.campaigns.append(campaign)
        return campaign.save()

    def delete_campaign(self, id):
        pass

    def info(self, msg):
        print('Hi {}, message for you: {}'.format(self, msg))

    def save(self):
        self.id = self.user_mapper.insert(self)
