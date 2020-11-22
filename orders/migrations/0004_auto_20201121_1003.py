# Generated by Django 3.1.3 on 2020-11-21 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_dish_image'),
        ('orders', '0003_auto_20201121_0059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooksorders',
            name='orders',
        ),
        migrations.AddField(
            model_name='cooksorders',
            name='orders',
            field=models.ManyToManyField(to='menu.Dish'),
        ),
    ]
