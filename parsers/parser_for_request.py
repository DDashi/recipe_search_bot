from bs4 import BeautifulSoup
import requests
import re
from .pages.page import Page

requests_re_img = r'/binfiles/images.*jpg|/binfiles/images.*png|/binfiles/images.*jpeg|/Content/images/noi_ph.png'
requests_re_title = r'class="material-anons__des">((.|\n)*)</p>'
requests_re_href = r'class="material-anons__title" href="(.*)</a>'

to_correct_url = 'https://www.gastronom.ru'

class ParserForRequest:
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.pages = []
        pages_data = self.soup.find_all('article')
        self.pages_count = 0
        if len(pages_data) != 0:
            self.pages_count = int(self.soup.find_all('strong')[0].__str__()[8:-9])

        for date in pages_data:
            img = re.findall(requests_re_img, date.__str__())[0]
            title = re.findall(requests_re_title, date.__str__())
            annotation = re.findall(requests_re_href, date.__str__())[0].split('>')
            href = annotation[0][:-1]
            description = annotation[1]
            page = Page(title[0][0], description, to_correct_url + img, to_correct_url + href)
            self.pages.append(page)

