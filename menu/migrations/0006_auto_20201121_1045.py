# Generated by Django 3.1.3 on 2020-11-21 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20201121_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='confirmed_orders',
            field=models.TextField(default='[]', null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='unconfirmed_orders',
            field=models.TextField(default='[]', null=True),
        ),
    ]
