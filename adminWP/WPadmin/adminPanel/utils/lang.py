import json
import csv
import re

import random
from random import Random
from adminPanel.models import Атрибуты, Значения_атрибутов, Поставщики, Категории
from adminPanel import views

MYFIELDS = [
    "parent", "type", 'Имя', 'Цена', 'Images', 'Categories', 'SKU', 'Tags', 'Tax class', "В наличии?"
]


def generate_sku():
    sku = random.randint(10000, 99999)
    return sku


def prepare_data(product):
    data = {}
    for name in Значения_атрибутов.objects.all():
        if str(name.Вариант1) in product or str(name.Вариант2) in product or str(name.Вариант3) in product or str(
                name.Вариант4) in product or str(name.Вариант5) in product or str(name.Вариант6) in product or str(
            name.Вариант7) in product or str(name.Вариант8) in product or str(name.Вариант9) in product or str(
            name.Вариант10) in product or str(name.Вариант11) in product or str(name.Вариант12) in product or str(
            name.Вариант13) in product or str(name.Вариант14) in product or str(name.Вариант15) in product or str(
            name.Вариант16) in product or str(name.Вариант17) in product or str(name.Вариант18) in product or str(
            name.Вариант19) in product or str(name.Вариант20) in product:
            data[str(name.Атрибут)] = str(name)
        else:
            continue
        for sup in Поставщики.objects.all():
            if str(sup.Поставщик) == product.split('\n')[0]:
                if str(sup.Атрибут1) != 'null':
                    data[str(sup.Атрибут1)] = str(sup.Вариант1)
                if str(sup.Атрибут2) != 'null':
                    data[str(sup.Атрибут2)] = str(sup.Вариант2)
                if str(sup.Атрибут3) != 'null':
                    data[str(sup.Атрибут3)] = str(sup.Вариант3)
                if str(sup.Атрибут4) != 'null':
                    data[str(sup.Атрибут4)] = str(sup.Вариант4)

        # if str(Поставщики.Атрибут1) != "null":
        #   data[str(Поставщики.Атрибут1)] = str(Поставщики.Вариант1)
    return data


def get_price(line):
    prices = []
    if 'цена' in line or 'руб' in line:
        price = ''
        for l in line:
            if l.isdigit():
                price += l
        if len(price) > 0:
            prices.append(int(price))
    return prices


def get_size(line):
    if 'размер' in line:
        size_list = []
        size = ''
        for i in range(len(line)):
            if line[i].isdigit():
                size += line[i]
            if i < len(line) - 1 and not line[i + 1].isdigit():
                if size:
                    size_list.append(size)

                    size = ''
        if size and size not in size_list:
            size_list.append(size)
            # print(size_list)
        for i in range(len(size_list)):
            try:
                size_list[i] = int(size_list[i])
            except:
                pass
        size_list = list(filter(lambda size: type(size) is int and 40 <= size <= 70, size_list))
        if size_list:
            return size_list


def get_length(line):
    length = ''
    if 'длина' in line or 'длинна' in line:
        for char in line:
            if char.isdigit():
                length += char
    if len(length) > 0:
        return int(length)


def format_prices(prices):
    if len(prices) < 1:
        return None
    else:
        if len(prices) == 1:
            if 100 <= prices[0] <= 9999:
                return [round(prices[0] * 1.4)]
        elif len(prices) == 2:
            if 100 <= prices[0] <= 9999 and 100 <= prices[1] <= 9999 and max(prices) <= min(prices) * 1.2:
                return [round(max(prices) * 1.4), min(prices)]


def get_categories(title, gender):
    for cat in Категории.objects.all():
        if title == str(cat.Название):
            if 'Женщинам' == gender:
                return str(cat.Категория_Женщинам)
            elif 'Мужчинам' == gender:
                return str(cat.Категория_Мужчинам)
            elif 'Унисекс' == gender:
                return str(cat.Категория_Унисекс)
            elif 'Мальчикам' == gender:
                return str(cat.Категория_Мальчикам)
            elif 'Девочкам' == gender:
                return str(cat.Категория_Девочкам)
            elif 'Деткам' == gender:
                return str(cat.Категория_Деткам)
            else:
                return ''


def get_image_size(line):
    pattern = r"size=(\d+)x(\d+)"
    result = re.search(pattern, line)
    return int(result.group(1)), int(result.group(2))


def get_data(product):
    urls = []
    sizes = []
    products = []
    length = []
    prices = []
    size = []

    for line in product.split("\n"):
        if line[:11] == 'https:\/\/s':
            urls.append(line)
        price = get_price(line)
        if len(price) > 0:
            prices.append(price)
        sizes.append(get_size(line))
        number = get_length(line)
        if number is not None:
            length.append(number)
        size.append(get_size(line))

    for i in range(len(urls)):
        url = urls[i]
        product_data = prepare_data(product)
        # if 'title' in product_data:
        # if 'платье' in product_data['title'].lower():
        # product_data['gender'] = 'Женщинам'
        product_data["url"] = url
        if len(length) > 0:
            product_data["length"] = length[0]
        if prices:
            price = prices[0]
            formatted = format_prices(price)
            if formatted is not None:
                if len(formatted) == 1:
                    product_data['price'] = formatted[0]
                elif len(formatted) == 2:
                    product_data['price'] = formatted[0]
                    product_data['price_opt'] = formatted[1]
        if size:
            for s in size:
                if s is not None:
                    real_size = list(set(s))
                    real_size.sort()
                    # real_size = str(real_size).replace('[', '')
                    # real_size = str(real_size).replace(']', '')
                    # product_data["size"] = str(real_size)
                    if 'title' in product_data:
                        for item in Значения_атрибутов.objects.all():
                            if product_data['title'] == item.Название:
                                edin = item.Единый_размер
                        if edin == True:
                            real_size = f"{product_data['size'][0]}-{product_data['size'][-1]}"

                        else:
                            product_data["size"] = real_size
        if ('title' in product_data) and ('gender' in product_data):
            product_data['categories'] = get_categories(product_data['title'], product_data['gender'])
        else:
            product_data['categories'] = ''
        if ('title' in product_data) and ('price' in product_data):
            products.append(data_refactoring(product_data))
    return products


def data_refactoring(data):
    edin = None
    for item in Значения_атрибутов.objects.all():
        if data['title'] == item.Название:
            edin = item.Единый_размер
    Attributes = []
    if not edin:
        for item in Атрибуты.objects.all():
            Attributes.append(str(item))
        if len(data['size']) > 1:
            product_data = {
                'name': data['title'],
                'type': 'variable',
                "sku": str(random_sku()),
                "images": [{
                    "src": data['url'],
                }],
                "categories": [
                    {
                        'id': str(data['categories']),
                    }
                ],
                "attributes": [
                    {
                        'name': 'Размер',
                        'variation': True,
                        'visible': True,
                        'options': [str(size) for size in data['size']]
                    }

                ]
            }


        for item in Attributes:
            if item != 'title':
                try:
                    attr_data = {
                        'name': str(item),
                        'visible': True,
                        'options': str(data[item])
                    }
                    product_data['attributes'].append(attr_data)
                except:
                    pass
        variant_data = {
            "regular_price": str(data['price']),
            "stock_quantity": "1000",
            'attributes': [{
                'name': 'Размер',
            }]
        }
        return product_data, variant_data
    else:
        product_data = {
            'name': data['title'],
            'type': 'simple',
            "sku": str(random_sku()),
            "images": [{
                "src": data['url'],
            }],
            "categories": [
                {
                    'id': str(data['categories']),
                }
            ],
            "attributes": [
                {
                    'name': 'Размер',
                    'visible': True,
                    'options': [str(size) for size in data['size']]
                }

            ]
        }

        for item in Attributes:
            if item != 'title':
                try:
                    attr_data = {
                        'name': str(item),
                        'visible': True,
                        'options': str(data[item])
                    }
                    product_data['attributes'].append(attr_data)
                except:
                    pass
        return product_data, ''


def random_sku():
    return random.Random().randint(10000, 99999)


def check_product(products):
    products_list = []
    for product in products:
        data = get_data(product)
        if len(data) > 1:
            for dubl in data:
                products_list.append(dubl)
        elif len(data) == 1:
            products_list.append(data[0])
    print(len(products_list))
    return products_list

# print(lang)
# lang = add_lang(lang, 'test', 'пиздец', 'тест')
