from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from adminPanel.utils import wooImport
from time import sleep, time
from adminPanel.models import Продукты


class Command(BaseCommand):
    'parce'

    def handle(self, *args, **kwargs):
        while True:
            product = AB()

            self.stdout.write("greet!")
            sleep(10)


def AB():
    # try:
    product = wooImport.get_context()
    for items in product:
        for item in items:
            now = time()
            picture = item[0]['images'][0]['src']
            flag = False
            for images in Продукты.objects.all():
                if picture == str(images.Картинка):
                    flag = True
            if not flag:
                product_id = wooImport.woocommerce_create_product(item[0], item[1])
                b = Продукты(Продукт=str(product_id), Дата=str(now), Картинка=picture)
                b.save()
    for item in Продукты.objects.all():
        now = time()
        if float(item.Дата) < now:
            wooImport.woocomerce_delete_product(item.Продукт)
    # print("=" * 100, product)
    return product
    # '''except:
    #     return "Нету пола"'''
