# Generated by Django 3.1.3 on 2021-01-30 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_auto_20210128_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('time_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('time_added',),
            },
        ),
    ]
