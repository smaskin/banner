from banner.storage import Repository


class Position:
    def __init__(self, user_id, site):
        self.user_id = user_id
        self.site = site
        self.banners = []

    def get_id(self):
        return id(self)

    def get_hash(self):
        return hash(self.get_id)

    def assign_banner(self, banner):
        self.banners.append(banner)

    def deassign_banners(self, position, banner):
        pass

    def generate_widget_script(self):
        return '<script>let label = document.querySelectorAll("div[data-banner-label={}]");</script>'.format(self.get_hash())

    def generate_widget_label(self):
        return '<div data-banner-label="{}"></div>'.format(self.get_hash())

    def save(self):
        repository = Repository()
        repository.insert(Repository.TYPE_POSITION, self)
