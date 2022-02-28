from django.contrib import admin
from .models import Значения_атрибутов, Атрибуты, Категории, Поставщики, Продукты

# Register your models here.
admin.site.register(Значения_атрибутов)
admin.site.register(Атрибуты)
admin.site.register(Категории)
admin.site.register(Поставщики)
admin.site.register(Продукты)