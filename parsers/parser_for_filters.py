from bs4 import BeautifulSoup
import requests
import re
import json
import os

def write_file(name, date):
    with open(os.path.join(os.path.dirname(__file__), 'filters',  name), "w", encoding='utf-8') as file:
        json.dump(date, file, ensure_ascii=False)

url = 'https://www.gastronom.ru/recipe'

type_of_dish = {}
type_of_kitchen = {}
amount_of_time = {}

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parsers')

for option in soup.find_all('option'):
    numbers = re.findall(r'\d{1,3}', option.__str__())
    count = numbers[0]
    text = option.text
    if text == 'Более 2 часов':
        amount_of_time[text] = count
    elif len(numbers) == 1 and int(count) <= 10:
        type_of_dish[text] = count
    elif len(numbers) == 1:
        type_of_kitchen[text] = count
    else:
        amount_of_time[text] = f"{count}-{numbers[1]}"

write_file("type_of_dish.json", type_of_dish)
write_file("type_of_kitchen.json", type_of_kitchen)
write_file("amount_of_time.json", amount_of_time)
