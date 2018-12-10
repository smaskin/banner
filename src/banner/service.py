from banner.dto import BannerDTO
from banner.mapper import BannerMapper
from banner.entity import Banner


class BannerService:
    def __init__(self):
        self.banner_mapper = BannerMapper()

    def create(self, user, campaign, post):
        banner = Banner.create(user, campaign, BannerDTO(post))
        self.banner_mapper.insert(banner)
        return banner
