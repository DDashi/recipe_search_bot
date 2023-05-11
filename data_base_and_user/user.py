class User:
    def __init__(self, from_dict=None):
        if from_dict is not None:
            for key in from_dict:
                setattr(self, key, from_dict[key])
        else:
            self.recipes = []

    def update(self, recipe):
        self.recipes.append(recipe)

    def __str__(self):
        return self.recipes.__str__()

    def __dict__(self):
        return {"recipes": self.recipes}
