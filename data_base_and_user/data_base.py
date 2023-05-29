import json
from .user import User

path = 'data_base_and_user\\users.json'

class DataBase:
    def __init__(self):
        self.users = {}
        with open(path) as f:
            json_content = json.load(f)
        for id, data in json_content.items():
            user = User(from_dict=data)
            self.users[id] = user

    def create(self, id, message_id, message_text, recipe_number=None):
        if id not in self.users:
            self.users[id] = User(message_id, message_text)
        else:
            self.update_message_id(id, message_id, message_text, recipe_number)


    def update_message_id(self, id, message_id, message_text, recipe_number=None):
        id = str(id)
        self.users[id].update_message_id(message_id, message_text, recipe_number)


    def get_user(self, id):
        id = str(id)
        return self.users[id]

    def get_recipes(self, id):
        id = str(id)
        return self.users[id].recipes

    def save(self):
        deserialize_users = {}
        for ip, user in self.users.items():
            deserialize_users[ip] = user.__dict__()
        with open(path, "w") as file:
            json.dump(deserialize_users, file)
