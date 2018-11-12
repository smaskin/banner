class Position:
    banners = []

    def __init__(self, user_id, site):
        self.user_id = user_id
        self.site = site

    def get_id(self):
        return id(self)

    def get_hash(self):
        return hash(self.get_id)

    def assignBanner(self, banner):
        self.banners.append(banner)

    def generateWidgetScript(self):
        return '<script>let label = document.querySelectorAll("div[data-banner-label={}]");</script>'.format(self.get_hash())

    def generateWidgetLabel(self):
        return '<div data-banner-label="{}"></div>'.format(self.get_hash())

    def save(self):
        pass
