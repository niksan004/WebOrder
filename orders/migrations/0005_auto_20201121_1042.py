# Generated by Django 3.1.3 on 2020-11-21 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20201121_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooksorders',
            name='orders',
        ),
        migrations.AddField(
            model_name='cooksorders',
            name='orders',
            field=models.TextField(null=True),
        ),
    ]