# Generated by Django 3.1.3 on 2021-05-16 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_dish_allergens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='allergens',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
