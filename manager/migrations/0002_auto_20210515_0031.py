# Generated by Django 3.1.3 on 2021-05-15 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PayedTable',
            new_name='PaidTable',
        ),
    ]