import re

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from time import sleep
from os.path import exists
from datetime import datetime, timedelta

class VK(object):

    def __init__(self, url: str = 'https://vk.com/sadovod_postavshiki') -> None:
        self.r: requests.Session = requests.Session()
        self.url: str = url
        self.urls: list = []
        self.date: list = []
        self.suppliers: list = []
        self.walls: list = []
        self.post: str = ''
        self.products: list = []
        self.response: str = ''
        self.headers: dict = {
            'User-Agent': UserAgent().random,
            'Accept-Language': 'ru',
        }

    # Запрос с обработкой блокировки
    def get_response(self) -> None:
        while True:
            try:
                # self.response = httpx.get(self.url, headers=self.headers).text
                # with httpx.Client(headers=self.headers) as client:
                #     self.response = client.get(self.url).text
                self.response = self.r.get(self.url, headers=self.headers).text
                # self.response = self.response.text
                self.soup = bs(self.response, 'lxml')
                break
            except:
                sleep(3)

    # Получение списка поставщиков
    def get_suppliers(self) -> None:
        self.url = 'https://vk.com/sadovod_postavshiki'
        self.get_response()
        self.suppliers = []
        walls: str = list(filter(lambda wall: 'wall' in wall, [wall.find('a')['href'] for wall in
                                                               self.soup.find_all('td',
                                                                                  class_='app_widget_table_td app_widget_linked')]))
        for wall in walls:
            offset = 0
            while True:
                self.url = f"https://vk.com{wall[:wall.find('?') + 1] + f'offset={offset}&' + wall[wall.find('?') + 1:]}"
                self.get_response()

                if not (posts := self.soup.find_all('div', class_='wall_post_text')):
                    break
                offset += 20
                self.suppliers += list(filter(lambda post: 'wall-166887822' not in post and 'vk.com/' in post,
                                              [post.find('a')['href'] for post in posts]))
            # sleep(1)
        # self.save_walls()
        self.suppliers = list(map(lambda url: url.replace('http://', 'https://').replace('m.vk.com', 'vk.com'),
                                  list(set(self.suppliers))))
        self.save_suppliers()

    # Сохранение списка поставщиков
    def save_suppliers(self, suppliers_file: str = 'suppliers.txt') -> None:
        with open(suppliers_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(self.suppliers))

    # Загрузка списка поставщиков из файла
    def upload_suppliers(self, suppliers_file: str = 'suppliers.txt') -> None:
        if exists(suppliers_file):
            with open(suppliers_file, 'r', encoding='utf-8') as file:
                self.suppliers = [supplier.strip() for supplier in file]
        else:
            raise ValueError('Не существует файла поставщиков!')

    def upload_walls(self):
        if exists('walls.txt'):
            with open('walls.txt', 'r', encoding='utf-8') as file:
                self.walls = [wall.strip() for wall in file]
        else:
            raise ValueError('Не существует файл с постами')

    def save_walls(self):
        with open('walls.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(self.walls))

    def get_posts(self, url: str) -> None:
        self.url = url
        self.get_response()
        print(self.url)
        if self.soup.find('li', class_='_wall_tab_own'):
            return self.soup.find('li', class_='_wall_tab_own').find('a')['href']

    def delta_date(self, date: str, minute: int = None, hour: int = None, day: int = None) -> bool:
        print(date)
        try:
            if int(date[2:4]) > datetime.now().month:
                date = date[:7] + str(int(date[7]) + 1) + date[8:]
        except:
            return False
        delta = datetime.now() - datetime.strptime(date, '%d%m%Y%H%M')

        if minute:
            return delta.total_seconds() / 60 < minute
        elif hour:
            return delta.total_seconds() / 3600 < hour
        elif day:
            return delta.days < day
        else:
            raise ValueError('Не передан промежуток времени!')

    def post_date(self, date: str, minute: int = None, hour: int = None, day: int = None) -> bool:
        month = {
            ' янв в ': '01',
            ' фев в ': '02',
            ' мар в ': '03',
            ' апр в ': '04',
            ' май в ': '05',
            ' июн в ': '06',
            ' июл в ': '07',
            ' авг в ': '08',
            ' сен в ': '09',
            ' окт в ': '10',
            ' ноя в ': '11',
            ' дек в ': '12',
        }

        if 'сегодня в ' in date or 'вчера в ' in date:
            # добавить для вчера
            date = datetime.strftime(datetime.now(), '%d%m%Y') + date.replace('сегодня в ', '').replace('вчера в ',
                                                                                                        '').replace(':',
                                                                                                                    '')
            return self.delta_date(date, day=30)
        elif u' ' not in date:
            date = '0' + date if date[1] == ' ' else date
            date = date[:9] + '0' + date[9:] if len(date) == 13 else date
            # print(date)
            for m in month:
                if m in date:
                    date = date.replace(m, month[m])
                    break
            date = date[:-5] + f'{datetime.now().year}' + date[-5:].replace(':', '')
            return self.delta_date(date, day=30)
        else:
            return False

    def strip_product(self, product: str) -> str:
        return '\n'.join(map(lambda prod: prod.strip(), filter(lambda prod: not prod.isspace(), product.split('\n'))))

    def get_products(self, url: str,supplier, minute: int = None, hour: int = None, day: int = None):
        self.url = url
        self.get_response()
        self.products = []
        self.date = []
        content = self.soup.find_all('div', class_='post_content')
        # try:
        for date in self.soup.find_all('div', class_='post_date'):
            self.date.append(self.post_date(date.find('span')['abs_time']) if 'abs_time' in date.find(
                'span').attrs else self.post_date(date.find('span').text))
        print(self.date)

        for i in range(len(content)):
            for post in content:
                cont_soup = bs(str(post), 'lxml')

                text = cont_soup.find('div', class_='wall_post_text')
                photo = cont_soup.find_all("a", {"aria-label": "фотография"})
                links = []
                if photo:
                    urls = re.findall(r"(https:\S{150,200}album)&quot", str(photo).replace(";", "&"))
                    bigest = None
                    new_urls = []
                    for url in urls:
                        str1 = re.findall(r"https:.{10,50}\\/(.+)\\/",url)
                        new_urls.append(str1[0])
                    new_urls = set(new_urls)
                    new_urls = list(new_urls)
                    new_urls2 = []
                    for str1 in new_urls:
                        greet = []
                        for url in urls:
                            if str1 in url:
                                greet.append(url)
                        new_urls2.append(greet)
                    for list1 in new_urls2:
                        sizes = re.findall(r"size=(\d+)x(\d+)", str(list1))
                        for size in sizes:
                            if bigest is None:
                                bigest = size
                            elif int(size[0]) * int(size[1]) > int(bigest[0]) * int(bigest[1]):
                                bigest = size
                        str11 = 'size='+str(bigest[0])+'x'+str(bigest[1])
                        for url in list1:
                            if str11 in url:
                                sleep(0.01)
                                links.append(url)
                    links = set(links)
                    links = list(links)
                    new_links = ''
                    for link in links:
                        new_links += link+'\n'
                if self.date[i]:
                    try:
                        product = supplier + "\n" + self.strip_product(text.get_text(separator='\n')).lower()+"\n"+str(new_links)
                        self.products.append(product)
                    except:
                        print("error")

            break
        return self.products
        # except:
        #     pass

    def rewrite_post(self, post: str) -> str:
        post = [list(map(lambda post: post.lower().strip(), post.split())) for post in post.split('\n')]
        for i in range(len(post)):
            for j in range(len(post[i])):
                k = 0
                while k < len(post[i][j]):
                    if not post[i][j][k].isalnum():
                        post[i][j] = post[i][j].replace(post[i][j][k], '')
                    else:
                        k += 1

    #def main(self) -> None:
        #self.get_suppliers()
        #for supplier in self.suppliers:
         #   self.get_posts(supplier)
        #self.save_walls()
        # print(self.get_url(open("probe.txt", "r", encoding="utf-8")))
     #   self.upload_walls()
      #  for wall in self.walls:
       #     wall = 'https://vk.com' + wall[:-6] + "?offset=1&own=1"
        #    #wall = 'https://vk.com' + wall[:-6] + '?offset=20&own=1'
         #   self.get_products(wall, day=10)

#vk = VK()
#if __name__ == '__main__':
    #upload_lang()
    #vk.get_suppliers()
    #vk.save_suppliers()
    #vk.upload_suppliers()
    #vk.main()
# vk.upload_walls()

#     vk.url = 'https://vk.com//wall566695290?own=1'
# # vk.get_response()
#     vk.get_products('https://vk.com/wall528247126?offset=20&own=1', day=10)
# vk.rewrite_post('''Новинка Обложка на паспорт
# материал кожа натуральный 100%
# качество люкс
# в комплекте коробка пыльник
# размер Стандарт для паспорта,
# цена 1000₽
# Адрес тк садовод 23,87,
# тел 89268644566WhatsApp''')
