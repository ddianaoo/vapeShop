from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, null=False, verbose_name='Назва')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, null=False, verbose_name='Назва')
    description = models.TextField(blank=True, verbose_name='Опис')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія')
    production = models.CharField(max_length=255, null=False, verbose_name='Виробник')
    price = models.IntegerField(null=False, verbose_name='Ціна')
    stock_quantity = models.IntegerField(null=False, verbose_name='Кількість у наявності')

    def __str__(self):
        return self.title
