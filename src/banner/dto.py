import datetime
from banner.entity import Period, Limiter, Regions


class BannerDTO:
    def __init__(self, post):
        self.image_url = post['image_url'] if 'image_url' in post else None
        self.content = post['content'] if 'content' in post else None
        self.regions = Regions(post['regions']) if 'regions' in post else Regions()
        self.allowed = post['allowed'] if 'allowed' in post else True

        start = post['start'] if 'start' in post else datetime.datetime.now()
        finish = post['finish'] if 'finish' in post else datetime.datetime.now() + datetime.timedelta(weeks=1)
        self.period = Period(start, finish)

        show_limit = post['show_limit'] if 'show_limit' in post else 0
        click_limit = post['click_limit'] if 'click_limit' in post else 0
        self.limiter = Limiter(show_limit, click_limit)
