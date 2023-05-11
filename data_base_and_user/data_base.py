import json
from user import User

path = 'data_base_and_user\\users.json'

class DataBase:
    def __init__(self):
        self.users = {}
        with open(path) as f:
            json_content = json.load(f)
        for id, data in json_content.items():
            user = User(from_dict=data)
            self.users[id] = user

    def create(self, id):
        if id not in self.users:
            self.users[id] = User()

    def get_user(self, id):
        return str(self.users[id])

    def get_recipes(self, id):
        return self.users[id].recipes

    def save(self):
        deserialize_users = {}
        for ip, user in self.users.items():
            deserialize_users[ip] = user.__dict__()
        with open(path, "w") as file:
            json.dump(deserialize_users, file)
