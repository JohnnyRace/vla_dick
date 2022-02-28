from django.db import models


class Атрибуты(models.Model):
    Название_атрибута = models.CharField(max_length=30)

    def __str__(self):
        return self.Название_атрибута


class Значения_атрибутов(models.Model):
    Название = models.CharField(max_length=30)
    Единый_размер = models.BooleanField(default=False)
    Атрибут = models.ForeignKey(Атрибуты, on_delete=models.CASCADE)
    Вариант1 = models.CharField(max_length=30, null=True, blank=True)
    Вариант2 = models.CharField(max_length=30, null=True, blank=True)
    Вариант3 = models.CharField(max_length=30, null=True, blank=True)
    Вариант4 = models.CharField(max_length=30, null=True, blank=True)
    Вариант5 = models.CharField(max_length=30, null=True, blank=True)
    Вариант6 = models.CharField(max_length=30, null=True, blank=True)
    Вариант7 = models.CharField(max_length=30, null=True, blank=True)
    Вариант8 = models.CharField(max_length=30, null=True, blank=True)
    Вариант9 = models.CharField(max_length=30, null=True, blank=True)
    Вариант10 = models.CharField(max_length=30, null=True, blank=True)
    Вариант11 = models.CharField(max_length=30, null=True, blank=True)
    Вариант12 = models.CharField(max_length=30, null=True, blank=True)
    Вариант13 = models.CharField(max_length=30, null=True, blank=True)
    Вариант14 = models.CharField(max_length=30, null=True, blank=True)
    Вариант15 = models.CharField(max_length=30, null=True, blank=True)
    Вариант16 = models.CharField(max_length=30, null=True, blank=True)
    Вариант17 = models.CharField(max_length=30, null=True, blank=True)
    Вариант18 = models.CharField(max_length=30, null=True, blank=True)
    Вариант19 = models.CharField(max_length=30, null=True, blank=True)
    Вариант20 = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.Название


class МенеджерАтрибутов(models.Manager):
    def attribute_list():
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Название FROM adminpanel_значения_атрибутов;""")
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row[0])
        print(result_list)
        return result_list


class Категории(models.Model):
    Название = models.ForeignKey(Значения_атрибутов, on_delete=models.CASCADE, verbose_name='Название')
    Категория_Мужчинам = models.CharField(max_length=100,blank=True)
    Категория_Женщинам = models.CharField(max_length=100, blank=True)
    Категория_Деткам = models.CharField(max_length=100, blank=True)
    Категория_Мальчикам = models.CharField(max_length=100, blank=True)
    Категория_Девочкам = models.CharField(max_length=100, blank=True)
    Категория_Унисекс = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.Название)


class Поставщики(models.Model):
    Поставщик = models.CharField(max_length=50)
    Атрибут1 = models.ForeignKey(Атрибуты, on_delete=models.CASCADE, related_name="Поставщики_Атрибут1",  blank=True)
    Вариант1 = models.CharField(max_length=50, blank=True)
    Атрибут2 = models.ForeignKey(Атрибуты, on_delete=models.CASCADE, related_name="Поставщики_Атрибут2",  blank=True)
    Вариант2 = models.CharField(max_length=50, blank=True)
    Атрибут3 = models.ForeignKey(Атрибуты, on_delete=models.CASCADE,related_name="Поставщики_Атрибут3", blank=True)
    Вариант3 = models.CharField(max_length=50, blank=True)
    Атрибут4 = models.ForeignKey(Атрибуты, on_delete=models.CASCADE,related_name="Поставщики_Атрибут4", blank=True)
    Вариант4 = models.CharField(max_length=50, blank=True)
    Номер_блока = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.Поставщик + ' ' + self.Номер_блока

class Продукты(models.Model):
    Продукт = models.CharField(max_length=500)
    Дата = models.CharField(max_length=30)
    Картинка = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Продукт + ' ' + self.Дата