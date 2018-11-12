from banner.banner import BannerFactory
from user.user import User

user = User('Test User')
user.createCampaign('Campaign #3')
campaign = user.campaigns[0]
user.createPosition('https://google.com')
user.createBanner(BannerFactory.TYPE_HTML, '<div>Content here</div>', campaign.get_id())
user.createBanner(BannerFactory.TYPE_IMAGE, 'https://www.gstatic.com/webp/gallery/1.jpg')
position = user.positions[0]
image_banner = user.banners[0]
html_banner = user.banners[1]
position.assignBanner(image_banner)
position.assignBanner(html_banner)
print(campaign.name)
print(position.generateWidgetScript())
print(position.generateWidgetLabel())
[print(banner.data) for banner in position.banners]

