import datetime


class Status:
    def __init__(self, banner, allowed):
        self.allowed = allowed
        self.banner = banner

    def is_active(self):
        return self.allowed and self.in_period() and self.in_limits() and self.in_region()

    def in_period(self):
        return self.banner.period.get_in(datetime.datetime.now())

    def in_limits(self):
        return self.banner.limiter.get_in(self.banner.get_show_count(), self.banner.get_click_count())

    def in_region(self):
        return self.banner.regions.match()
