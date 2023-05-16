import json
from .user import User

path = 'data_base_and_user\\users.json'

class DataBase:
    def __init__(self):
        self.users = {}
        with open(path) as f:
            json_content = json.load(f)
        for id, data in json_content.items():
            user = User(from_dict=data, message_id='-1')
            self.users[id] = user

    def create(self, id, message_id):
        if id not in self.users:
            self.users[id] = User(message_id)
        else:
            self.update_message_id(id, message_id)


    def update_message_id(self, id, message_id):
        self.users[id].update_message_id(message_id)


    def get_user(self, id):
        return self.users[id]

    def get_recipes(self, id):
        return self.users[id].recipes

    def save(self):
        deserialize_users = {}
        for ip, user in self.users.items():
            deserialize_users[ip] = user.__dict__()
        with open(path, "w") as file:
            json.dump(deserialize_users, file)
