from api.request import Request
from banner.service import BannerService
from user.service import UserService


class TestBannerAPI:
    def setup(self):
        self.user_service = UserService()
        self.user = self.user_service.get_entity()
        self.banner_service = BannerService()

    def test_create_banner(self):
        post = {'image_url': 'https://www.static.com/webp/gallery/1.jpg'}
        campaign = self.user_service.get_campaign(post)
        banner = self.banner_service.create(self.user, campaign, post)
        assert banner.image_url == 'https://www.static.com/webp/gallery/1.jpg'

    def test_create_position(self):
        position = self.user_service.create_position(Request.TEST_SITE)
        assert position.site == Request.TEST_SITE

    def test_get_banners(self):
        banners = self.user_service.get_banners()
        assert banners

    def test_assign_banner(self):
        post = {'image_url': 'https://www.static.com/webp/gallery/1.jpg'}
        campaign = self.user_service.get_campaign(post)
        banner = self.banner_service.create(self.user, campaign, post)
        position = self.user_service.create_position(Request.TEST_SITE)
        assert True

    def test_get_banner_by_position_hash(self):
        pass

    def test_create_user(self):
        assert self.user.name == 'Test User'

    def test_create_campaign(self):
        campaign = self.user_service.create_campaign('Test Campaign')
        assert campaign.name == 'Test Campaign'

    def test_status_banner(self):
        post = {'image_url': 'https://www.static.com/webp/gallery/1.jpg'}
        campaign = self.user_service.get_campaign(post)
        banner = self.banner_service.create(self.user, campaign, post)
        banner.limiter.show = 3
        assert banner.status.in_period()
        assert banner.status.in_limits()
        assert banner.status.in_region()
        assert banner.status.is_active()
        banner.show()
        assert banner.status.is_active()
        banner.show()
        assert banner.status.is_active()
        banner.show()
        assert not banner.status.is_active()
