# Generated by Django 3.1.3 on 2021-02-25 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-time_added',)},
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredients_bg',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredients_en',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='name_bg',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
