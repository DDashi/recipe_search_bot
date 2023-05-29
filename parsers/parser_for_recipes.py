from bs4 import BeautifulSoup
import requests
import re
from .pages.page import IMG

ingredients_with_heading = re.compile('recipe__ingredient')
cooking_time = re.compile('totalTime')
servings_count = re.compile('recipeYield')
requests_re_img = r'/binfiles/images.*jpg|/binfiles/images.*png|/binfiles/images.*jpeg|/Content/images/noi_ph.png'
requests_re_description = re.compile('recipe__step-text')
to_correct_url = 'https://www.gastronom.ru'
requests_heading = r'<div class="recipe__ingredient-title">'


class ParserForRecipes:
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.steps = []
        pages_data = self.soup.find_all(class_='recipe__step')
        list_of_ingredients_with_heading = self.soup.find_all(class_=ingredients_with_heading)
        list_of_ingredients_with_heading.pop()
        self.ingredients = ''

        for ingredient in list_of_ingredients_with_heading:
            ingredient = ingredient.__str__()
            if re.findall(requests_heading, ingredient) == []:
                self.ingredients += f'{ingredient[59:-5]}\n'
            else:
                self.ingredients += f'{ingredient[38:-6]}:\n'

        img = re.findall(requests_re_img,self.soup.find(itemprop="image").__str__())[0]
        self.cooking_time = self.soup.find(itemprop=cooking_time).__str__()[88:-6]
        self.servings_count = self.soup.find(itemprop=servings_count).__str__()[61:-6]

        self.steps.append(IMG(description=f'Время приготовления: {self.cooking_time}\n'
                                          f'Количество порций: {self.servings_count}\n'
                                          f'{self.ingredients}',
                              img=to_correct_url + img))

        for date in pages_data:

            img = re.findall(requests_re_img, date.__str__())
            description_soup = BeautifulSoup(date.__str__(), 'html.parser')
            description = description_soup.find_all(class_=requests_re_description)[0].__str__()[35:-10]
            step = None
            if img != []:
                step = IMG(description=description, img=to_correct_url + img[0])
            else:
                step = IMG(description=description)

            self.steps.append(step)
