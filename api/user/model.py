from banner.model import BannerFactory
from user.campaign import Campaign
from user.position import Position


class User:
    def __init__(self, name):
        self.name = name
        self._default_campaign = Campaign(self, 'Default campaign for {}'.format(name))

        self.banners = []
        self.positions = []
        self.campaigns = []

    def get_id(self):
        return id(self)

    def create_banner(self, t, data, campaign_id=None):
        factory = BannerFactory()
        banner = factory.create(self.get_id(), t, data, campaign_id if campaign_id else self._default_campaign.get_id())
        self.banners.append(banner)
        return banner.save()

    def delete_banner(self, id):
        pass

    def create_position(self, site_name: str):
        position = Position(self.get_id(), site_name)
        self.positions.append(position)
        return position.save()

    def delete_position(self, id):
        pass

    def create_campaign(self, name: str):
        campaign = Campaign(self.get_id(), name)
        self.campaigns.append(campaign)
        return campaign.save()

    def delete_campaign(self, id):
        pass
