import time
import pytest

from api.request import Request
from banner.forms import Form
from banner.model import Banner
from banner.proxy import CachedProxy, AuthProxy
from banner.storage import Repository
from user.model import User


class TestBannerAPI:
    def setup(self):
        self.user = User('Test User')
        self.repository = Repository()
        self.proxy = CachedProxy()
        self.auth = AuthProxy()

    def test_repository(self):
        self.user.create_position(Request.TEST_SITE)
        self.user.create_banner(Banner.TYPE_IMAGE, 'https://www.static.com/webp/gallery/1.jpg')
        self.user.positions[0].assign_banner(self.user.banners[0])
        position1_hash = self.user.positions[0].get_hash()
        assert self.repository.get_banners_by_position_hash(position1_hash)[0] == self.user.banners[0]

    def test_auth_proxy(self):
        self.user.create_position('https://ya.ru')
        self.user.create_banner(Banner.TYPE_IMAGE, 'https://www.static.com/webp/gallery/1.jpg')
        self.user.positions[0].assign_banner(self.user.banners[0])
        position1_hash = self.user.positions[0].get_hash()
        with pytest.raises(PermissionError):
            self.auth.get_banners_by_position_hash(position1_hash)

    def test_cache_proxy(self):
        self.user.create_position(Request.TEST_SITE)
        self.user.create_banner(Banner.TYPE_IMAGE, 'https://www.static.com/webp/gallery/1.jpg')
        self.user.positions[0].assign_banner(self.user.banners[0])
        position1_hash = self.user.positions[0].get_hash()
        start = time.time()
        assert self.proxy.get_banners_by_position_hash(position1_hash)[0] == self.user.banners[0]
        assert time.time() - start > Repository.TIMEOUT_FOR_TEST
        start = time.time()
        assert self.proxy.get_banners_by_position_hash(position1_hash)[0] == self.user.banners[0]
        assert time.time() - start < Repository.TIMEOUT_FOR_TEST


class TestUserAPI:
    def setup(self):
        self.user = User('Test User')

    def test_create_user(self):
        assert self.user.name == 'Test User'

    def test_create_campaign(self):
        self.user.create_campaign('Test Campaign')
        assert self.user.campaigns[0].name == 'Test Campaign'

    def test_create_position(self):
        self.user.create_position(Request.TEST_SITE)
        assert self.user.positions[0].generate_widget_script().startswith('<script>')
        assert self.user.positions[0].generate_widget_label().startswith('<div')

    def test_create_banner(self):
        self.user.create_campaign('Test Campaign')
        self.user.create_banner(Banner.TYPE_HTML, '<div>Content here</div>', self.user.campaigns[0])
        assert self.user.banners[0].get_json()['content'] == '<div>Content here</div>'
        with pytest.raises(TypeError):
            self.user.create_banner(999, '<div>Content here</div>', self.user.campaigns[0])

    def test_create_banner_with_default_campaign(self):
        self.user.create_banner(Banner.TYPE_IMAGE, 'https://www.gstatic.com/webp/gallery/1.jpg')
        assert self.user.banners[0].get_json()['image_url'] == 'https://www.gstatic.com/webp/gallery/1.jpg'

    def test_assign_banner(self):
        self.user.create_position(Request.TEST_SITE)
        self.user.create_banner(Banner.TYPE_IMAGE, 'https://www.static.com/webp/gallery/1.jpg')
        self.user.positions[0].assign_banner(self.user.banners[0])
        assert self.user.positions[0].banners[0].get_json()['image_url'].startswith('https://www.static')

    def test_status_banner(self):
        self.user.create_banner(Banner.TYPE_IMAGE, 'https://www.static.com/webp/gallery/1.jpg')
        banner = self.user.banners[0]
        banner.show_limit = 3
        assert banner.status.in_period()
        assert banner.status.in_show_limit()
        assert banner.status.in_click_limit()
        assert banner.status.in_limits()
        assert banner.status.in_region()
        assert banner.status.is_active()
        banner.show()
        assert banner.status.is_active()
        banner.show()
        assert banner.status.is_active()
        banner.show()
        assert not banner.status.is_active()

    # TODO create banner from form
    def test_banner_form(self):
        html_banner_form = Form.create(Form.TYPE_HTML, {'campaign': 'Test Campaign', 'content': '<div>Content here</div>'})
        assert html_banner_form
