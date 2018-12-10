from api.session import Session
from user.mapper import UserMapper


class UserService:
    def __init__(self):
        self.session = Session()
        self.user_mapper = UserMapper()
        self.user = self.get_entity()

    def get_entity(self):
        user_id = self.session.get_user_id()
        return self.user_mapper.get(user_id)

    def create(self, name):
        return self.user_mapper.insert(name)

    def get_campaign(self, post):
        if 'campaign_id' in post:
            return self.user_mapper.get_campaign(self.user, post['campaign_id'])
        if 'campaign_name' in post:
            return self.create_campaign(post['campaign_name'])
        return self.user_mapper.get_campaign(self.user)

    def create_campaign(self, name):
        return self.user_mapper.create_campaign(self.user, name)

    def create_position(self, site_name):
        return self.user_mapper.create_position(self.user, site_name)

    def get_position(self, _id):
        return self.user_mapper.get_position(self.user, _id)

    def get_banners(self):
        return self.user_mapper.get_banners(self.user)

    def get_banners_by_positions(self, position_id):
        position = self.user_mapper.get_position(self.user, position_id)
        return self.user_mapper.get_banners_by_positions(self.user, position)
