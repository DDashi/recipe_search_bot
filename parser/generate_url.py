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


path_to_filters = 'filters'  # 'parser\\filters'


def generate_url(name=None, types=None, kitchen=None, iningr=None, exingr=None, time=None, veget=None):
    url = 'https://www.gastronom.ru/search/type/recipe?tmp=1'
    if name is not None:
        url += f'&title={name}'

    if iningr is not None:
        url += f'&iningr={",".join(combine_filters_by_ingr(iningr))}'

    if exingr is not None:
        url += f'&exingr={",".join(combine_filters_by_ingr(exingr))}'

    if kitchen is not None:
        path = '\\type_of_kitchen.json'
        url += f'&kitchen={",".join(combine_filters(kitchen, path))}'

    if types is not None:
        path = '\\type_of_dish.json'
        url += f'&type={",".join(combine_filters(types, path))}'

    if time is not None:
        path = '\\amount_of_time.json'
        url += f'&time={",".join(combine_filters(time, path))}'

    if veget:
        url += f'&veget=17,16,15,19,18'
    return url


#if __name__ == '__main__':
#    print(generate_url(types=['салат', 'суп', 'второе блюдо'],
#                       kitchen=['домашняя', 'европейская'],
#                       iningr=['курица', 'сыр'],
#                       exingr=['лук'],
#                       time=['20-40 минут', '40-60 минут', '60-90 минут', '90-120 минут']))
#    print(generate_url(veget=True))
