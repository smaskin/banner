from api.request import Request
from banner.service import BannerService
from user.service import UserService


class UserController:
    def __init__(self):
        self.request = Request()
        self.banner_service = BannerService()
        self.user_service = UserService()

    def create_campaign(self):
        return self.user_service.create_campaign(self.request.post('name'))

    def create_banner(self):
        user = self.user_service.get_entity()
        campaign = self.user_service.get_campaign(self.request.post())
        return self.banner_service.create(user, campaign, self.request.post())

    def create_position(self):
        return self.user_service.create_position(self.request.post('site_name'))

    def get_position(self, _id):
        return self.user_service.get_position(_id)

    def get_banners(self):
        return self.user_service.get_banners()

    def get_banners_by_position(self, position_id):
        return self.user_service.get_banners_by_positions(position_id)
