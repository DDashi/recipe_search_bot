from .recipe_page import Recipe, IMG

class Page:
    def __init__(self, title, description, img, href):
        self.title = title
        self.img = IMG(img=img, description=description)
        self.href = href
