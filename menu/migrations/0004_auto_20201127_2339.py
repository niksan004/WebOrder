# Generated by Django 3.1.3 on 2020-11-27 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_table_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='check',
            field=models.FloatField(default=0),
        ),
    ]
