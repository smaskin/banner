class Campaign:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def get_id(self):
        return id(self)

    def save(self):
        pass
