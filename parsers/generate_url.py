import json


def open_file(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def combine_filters(types, file_path):
    numbers = []
    for filter_type in types:
        content: dict = open_file(path_to_filters + file_path)
        if filter_type in content:
            numbers.append(content[filter_type])
        else:
            raise Exception("Такого блюда нет")
    return numbers


def combine_filters_by_ingr(ingr):
    numbers = []
    for ingredient in ingr:
        numbers.append(ingredient)
    return numbers


path_to_filters = 'parsers\\filters'  # 'filters'


def generate_url(name=None, types=None, kitchen=None, iningr=None, exingr=None, time=None, veget=None):
    url = 'https://www.gastronom.ru/search/type/recipe?tmp=1'
    if name is not None and len(name) != 0:
        url += f'&title={name}'

    if iningr is not None and len(iningr) != 0:
        url += f'&iningr={",".join(combine_filters_by_ingr(iningr))}'

    if exingr is not None and len(exingr) != 0:
        url += f'&exingr={",".join(combine_filters_by_ingr(exingr))}'

    if kitchen is not None and len(kitchen) != 0:
        path = '\\type_of_kitchen.json'
        url += f'&kitchen={",".join(combine_filters(kitchen, path))}'

    if types is not None and len(types) != 0:
        path = '\\type_of_dish.json'
        url += f'&type={",".join(combine_filters(types, path))}'

    if time is not None and len(time) != 0:
        path = '\\amount_of_time.json'
        url += f'&time={",".join(combine_filters(time, path))}'

    if veget:
        url += f'&veget=17,16,15,19,18'
    return url
