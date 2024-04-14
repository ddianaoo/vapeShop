from django.db import models
from accounts.models import CustomUser

STATUS_CHOICES = (
    (0, 'Створюється'),
    (1, 'В обробці'),
    (2, 'Відправлено'),
    (3, 'Доставлено'),
)


class Category(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True, verbose_name='Назва')

    class Meta:
        verbose_name = 'категорія'
        verbose_name_plural = 'категорії'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, null=False, verbose_name='Назва')
    description = models.TextField(blank=True, verbose_name='Опис')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія')
    production = models.CharField(max_length=100, null=False, verbose_name='Виробник')
    price = models.IntegerField(null=False, verbose_name='Ціна')
    stock_quantity = models.IntegerField(null=False, verbose_name='Кількість у наявності')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товар'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата створення')
    status = models.CharField(null=False, choices=STATUS_CHOICES, default=0)

    class Meta:
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'
        ordering = ['-created_at']


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
