import abc
import datetime


class Status(metaclass=abc.ABCMeta):
    def __init__(self, banner):
        self.banner = banner

    @abc.abstractmethod
    def is_active(self):
        pass

    @abc.abstractmethod
    def click(self):
        pass

    @abc.abstractmethod
    def show(self):
        pass


class PublishedStatus(Status):
    def click(self):
        if not self.in_limits():
            self.banner.change_status(ForbiddenStatus(self.banner))

    def show(self):
        if not self.in_limits():
            self.banner.change_status(ForbiddenStatus(self.banner))

    def is_active(self):
        return self.banner.allowed and self.in_period() and self.in_limits() and self.in_region()

    def in_period(self):
        return self.banner.start < datetime.datetime.now() < self.banner.finish

    def in_limits(self):
        return self.in_show_limit() and self.in_click_limit()

    def in_show_limit(self):
        return self.banner.show_limit == 0 or self.banner.get_show_count() < self.banner.show_limit

    def in_click_limit(self):
        return self.banner.click_limit == 0 or self.banner.get_click_count() < self.banner.click_limit

    def in_region(self):
        from api.request import Request
        request = Request()
        return request.region in self.banner.regions


class ForbiddenStatus(Status):
    def click(self):
        self.inform('click')

    def show(self):
        self.inform('show')

    def inform(self, t):
        self.banner.user.info('Banner {} was {}ed out of limit'.format(self.banner, t))

    def is_active(self):
        return False
