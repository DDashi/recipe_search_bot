class User:
    def __init__(self,message_id, from_dict=None):
        if from_dict is not None:
            for key in from_dict:
                setattr(self, key, from_dict[key])
        else:
            self.recipes = []
            self.message_id = message_id

    def update(self, recipe):
        self.recipes.append(recipe)

    def update_message_id(self, id):
        self.message_id = id

    def __str__(self):
        return self.recipes.__str__()

    def __dict__(self):
        return {"recipes": self.recipes, "message_id": self.message_id}
