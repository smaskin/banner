from user.model import User
from user.position import Position


class UserMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get(self, _id):
        statement = f"SELECT * FROM user WHERE id='{_id}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchone()
        if result:
            return User(result[0])
        else:
            raise Exception(f'record with id={_id} not found')

    def insert(self, model):
        self.cursor.execute(f"INSERT INTO user (name) VALUES ('{model.name}')")
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
        return self.cursor.lastrowid


class PositionMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def insert(self, model):
        self.cursor.execute(f"INSERT INTO position (hash, user_id, site) VALUES ('{model.get_hash()}', '{model.user_id}', '{model.site}')")
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
        return self.cursor.lastrowid

    def get(self, _hash):
        statement = f"SELECT id, user_id, site FROM position WHERE hash='{_hash}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchone()
        if result:
            return Position(result[1], result[2], _id=result[0])
        else:
            raise Exception(f'record with hash={_hash} not found')


class BannerMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def insert(self, model):
        self.cursor.execute(f"INSERT INTO banner (data, user_id) VALUES ('{model.data}', '{model.user.get_id()}')")
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

    def find_by_position(self, position):
        statement = f"SELECT banner.user_id, banner.data FROM banner_position LEFT JOIN banner ON banner.id = banner_position.banner_id WHERE banner_position.position_id='{position.get_id()}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        print(result, position.get_id())
        from banner.model import Banner
        if result:
            return [Banner.create(item[0], Banner.TYPE_IMAGE if item[1].startswith('http') else Banner.TYPE_HTML, item[1]) for item in result]
        else:
            raise Exception(f'record with id={position.get_id()} not found')
