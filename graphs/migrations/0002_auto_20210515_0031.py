# Generated by Django 3.1.3 on 2021-05-15 00:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dishesbypopularity',
            options={'verbose_name_plural': 'Dishes by popularity'},
        ),
        migrations.AddField(
            model_name='dishesbypopularity',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dishesbypopularity',
            name='number_of_orders',
            field=models.CharField(max_length=1000),
        ),
    ]
