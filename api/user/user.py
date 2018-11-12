from banner.banner import BannerFactory
from user.campaign import Campaign
from user.position import Position


class User:
    banners = []
    positions = []
    campaigns = []

    def __init__(self, name):
        self._default_campaign = Campaign(self, 'Default campaign for {}'.format(name))

    def get_id(self):
        return id(self)

    def createBanner(self, t, data, campaign_id=None):
        factory = BannerFactory()
        banner = factory.create(self.get_id(), t, data, campaign_id if campaign_id else self._default_campaign.get_id())
        self.banners.append(banner)
        return banner.save()

    def deleteBanner(self, id):
        pass

    def createPosition(self, site_name: str):
        position = Position(self.get_id(), site_name)
        self.positions.append(position)
        return position.save()

    def deletePosition(self, id):
        pass

    def createCampaign(self, name: str):
        campaign = Campaign(self.get_id(), name)
        self.campaigns.append(campaign)
        return campaign.save()

    def deleteCampaign(self, id):
        pass
