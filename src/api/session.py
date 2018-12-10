class Session:
    TEST_USER_ID = 1

    def __init__(self):
        self.id = self.TEST_USER_ID

    def get_user_id(self):
        return self.id
