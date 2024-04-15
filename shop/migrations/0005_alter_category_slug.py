# Generated by Django 4.2.11 on 2024-04-15 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Url'),
        ),
    ]
