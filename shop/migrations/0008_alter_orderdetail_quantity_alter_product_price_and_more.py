# Generated by Django 4.2.11 on 2024-05-16 08:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Кількість у наявності'),
        ),
    ]
