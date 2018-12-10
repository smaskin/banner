import sqlite3


class BannerMapper:
    def __init__(self):
        self.connection = sqlite3.connect('db/sqlite.db')
        self.connection = self.connection
        self.cursor = self.connection.cursor()

    def insert(self, model):
        self.cursor.execute(f"INSERT INTO banner (user_id, data, campaign_id, regions, start, finish, show_limit, click_limit, allowed) VALUES ('{model.user.get_id()}', '{model.get_data()}', '{model.campaign.get_id()}', '{model.regions}', '{model.period.start}', '{model.period.finish}', '{model.limiter.show}', '{model.limiter.click}', '{model.status.allowed}')")
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
        return self.cursor.lastrowid

    def assign(self, position, banner):
        self.cursor.execute(f"INSERT INTO banner_position (position_id, banner_id) VALUES ('{position.get_id()}', '{banner.get_id()}')")
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
