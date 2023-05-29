class User:
    def __init__(self, message_id=None, message_text=None, recipe_number=None, from_dict=None):
        if from_dict is not None:
            for key in from_dict:
                setattr(self, key, from_dict[key])
        else:
            self.recipes = []
            self.message_id = message_id
            self.message_text = message_text
            self.recipe_number = recipe_number
    def update(self, recipe):
        if recipe in self.recipes:
            return True
        self.recipes.append(recipe)
        return False

    def remove(self, recipe_index):
        self.recipes.pop(recipe_index)

    def update_message_id(self, id, message_text, recipe_number=None):
        self.message_id = id
        self.message_text = message_text
        self.recipe_number = recipe_number

    def __str__(self):
        return self.recipes.__str__()

    def __dict__(self):
        return {"recipes": self.recipes, "message_id": self.message_id, "message_text": self.message_text, "recipe_number": self.recipe_number}
