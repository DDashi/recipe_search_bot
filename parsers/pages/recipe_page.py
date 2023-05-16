class IMG:
    def __init__(self, description, img=None):
        self.img = img
        self.description = description

class Recipe:
    def __init__(self, ingredients, time, steps, servings_count):
        self.ingredients = ingredients # dict
        self.cooking_time = time
        self.steps = steps # list with IMG
        self.servings_count = servings_count
