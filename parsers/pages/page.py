from .recipe_page import Recipe, IMG

class Page:
    def __init__(self, title, description, img, href, ingredients=None, time=None, steps=None, servings_count=None):
        self.title = title
        self.img = IMG(img=img, description=description)
        self.href = href
        self.recipe = Recipe(ingredients, time, steps, servings_count)
