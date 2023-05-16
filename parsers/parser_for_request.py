from bs4 import BeautifulSoup
import requests
import re
from .pages.page import Page

requests_re_img = r'/binfiles/images.*jpg|/binfiles/images.*png'
requests_re_title = r'class="material-anons__des">(.*)</p>'
requests_re_href = r'class="material-anons__title" href="(.*)</a>'

to_correct_url = 'https://www.gastronom.ru'

class ParserForRequest:
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.pages = []

        for date in self.soup.find_all('article'):
            img = re.findall(requests_re_img, date.__str__())[0]
            title = re.findall(requests_re_title, date.__str__())[0]
            annotation = re.findall(requests_re_href, date.__str__())[0].split('>')
            href = annotation[0][:-1]
            description = annotation[1]
            page = Page(title, description, to_correct_url + img, to_correct_url + href)
            self.pages.append(page)

