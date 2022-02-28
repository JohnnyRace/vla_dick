import random

from adminPanel.utils.vk_parser import VK
from adminPanel.utils import lang
from adminPanel.models import Поставщики
from woocommerce import API


def woocommerce_create_product(data, data1):
    wcapi = API(
        url="https://sadovodrynok.ru/",
        consumer_key="ck_22e6c75a4671b6dc930c0b5196919f82d67dbf3a",
        consumer_secret="cs_8dc8c83fa03c2a1b705f162c71bd216267a47486",
        wp_api=True,
        version="wc/v3"
    )
    # https://sadovodrynok.ru/product-category/detkam/devochkam/platya-devochkam/myfdsfsd

    result = wcapi.post("products", data).json()
    print(result)
    if data1 == '':
        pass
    else:
        wcapi.post("products/" + str(result['id']) + "/variations", data1).json()

    return result['id']

def woocomerce_delete_product(product_id):
    wcapi = API(
        url="https://sadovodrynok.ru/",
        consumer_key="ck_22e6c75a4671b6dc930c0b5196919f82d67dbf3a",
        consumer_secret="cs_8dc8c83fa03c2a1b705f162c71bd216267a47486",
        wp_api=True,
        version="wc/v3"
    )
    wcapi.delete(f"products/{product_id}", params={"force": True}).json()

def get_context():
    vk = VK()
    product = []
    product1 = []
    for item in Поставщики.objects.all():
        try:
            wall = 'https://vk.com' + vk.get_posts(item.Поставщик)[:-6] + "?offset=1&own=1"
            product.append(vk.get_products(str(wall), item.Поставщик, day=10))
        except:
            print("123")
    for item in product:
        product1.append(lang.check_product(item))
    return product1
