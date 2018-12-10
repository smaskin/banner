from banner.dto import BannerDTO
from banner.entity import Banner
from user.entity import User, Campaign, Position
import sqlite3


class UserMapper:
    def __init__(self):
        self.connection = sqlite3.connect('db/sqlite.db')
        self.cursor = self.connection.cursor()

    def get(self, _id):
        statement = f"SELECT name FROM user WHERE id='{_id}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchone()
        model = User(result[0])
        model.set_id(_id)
        if result:
            return model
        else:
            raise Exception(f'record with id={_id} not found')

    def insert(self, name):
        self.cursor.execute(f"INSERT INTO user (name) VALUES ('{name}')")
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
        model = User(name)
        model.set_id(self.cursor.lastrowid)
        return model

    def get_campaign(self, user, campaign_id=None):
        if not campaign_id:
            return Campaign(user)
        statement = f"SELECT campaign.name FROM campaign WHERE user_id='{user.get_id()}' AND id='{campaign_id}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchone()
        model = Campaign(user, result[0])
        model.set_id(campaign_id)
        if result:
            return model
        else:
            raise Exception(f'record with id={campaign_id} not found')

    def create_campaign(self, user, name):
        self.cursor.execute(f"INSERT INTO campaign (name, user_id) VALUES ('{name}', '{user.get_id()}')")
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
        model = Campaign(user, name)
        model.set_id(self.cursor.lastrowid)
        return model

    def create_position(self, user, site):
        model = Position(user, site)
        self.cursor.execute(f"INSERT INTO position (user_id, hash, site) VALUES ('{user.get_id()}', '{model.hash}', '{site}')")
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
        model.set_id(self.cursor.lastrowid)
        return model

    def get_position(self, user, _id):
        statement = f"SELECT position.site, position.hash FROM position WHERE user_id='{user.get_id()}' AND id='{_id}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchone()
        model = Position(user, result[0], result[1])
        model.set_id(_id)
        if result:
            return model
        else:
            raise Exception(f'record with id={_id} not found')

    def get_banners(self, user):
        statement = f"SELECT campaign_id, data, regions, start, finish FROM banner WHERE banner.user_id='{user.get_id()}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return self._map_banners(user, result)
        else:
            raise Exception(f'no records for user with id={user.get_id()}')

    def get_banners_by_positions(self, user, position):
        statement = f"SELECT banner.user_id, banner.data, banner.regions, banner.start, banner.finish FROM banner_position LEFT JOIN banner ON banner.id = banner_position.banner_id WHERE banner_position.position_id='{position.get_id()}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return self._map_banners(user, result)
        else:
            raise Exception(f'no records for user with id={user.get_id()}')

    def _map_banners(self, user, result):
        entities = []
        for item in result:
            dto = BannerDTO({
                'image_url' if item[1].startswith('http') else 'content': item[1],
                'regions': item[2],
                'start': item[3],
                'finish': item[4],
            })
            campaign = self.get_campaign(user, item[0] if item[0] else None)
            banner = Banner.create(user, campaign, dto)
            entities.append(banner)
        return entities
