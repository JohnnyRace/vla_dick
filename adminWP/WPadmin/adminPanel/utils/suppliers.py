import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from time import sleep

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
                print("err")
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
        return self.suppliers
