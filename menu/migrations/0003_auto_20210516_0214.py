# Generated by Django 3.1.3 on 2021-05-16 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20210515_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
