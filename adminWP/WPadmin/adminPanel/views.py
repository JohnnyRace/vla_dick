from django.shortcuts import render
from django.http import response
from .models import Поставщики
from django.db import models
from adminPanel.utils import wooImport
from apscheduler.schedulers.background import BackgroundScheduler
from adminPanel.utils.vk_parser import VK

product = []

def home(request):
    #product = wooImport.get_context()
    vk=VK()
    product = []
    for item in Поставщики.objects.all():
        #try:
        wall = 'https://vk.com' + vk.get_posts(item.Поставщик)[:-6] + "?offset=1&own=1"
        product.append(vk.get_products(str(wall), item.Поставщик, day=10))
        #except:
         #   print("123")
    url1 = "https://vk.com/sadovod_postavshiki"
    context = {
        "url": url1,
        "suppliers": Поставщики.objects.all(),
        "sup": None,
        "products": product,
    }
    return render(request, 'parser/home.html', context)