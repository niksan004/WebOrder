# Generated by Django 3.1.3 on 2020-11-27 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('cook', 'cook'), ('distributor', 'distributor'), ('admin', 'admin')], default='', max_length=11),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]