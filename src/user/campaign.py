class Campaign:
    def __init__(self, user, name):
        self.user_id = user.get_id()
        self.name = name

    def get_id(self):
        return id(self)

    def save(self):
        pass
