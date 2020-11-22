from django.db import models
import uuid


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.category}'


class Dish(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=2000)
    quantity = models.IntegerField(default=300)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Table(models.Model):
    url = models.UUIDField(default=uuid.uuid4)
    unconfirmed_orders = models.TextField(null=True, default='[]')
    confirmed_orders = models.TextField(null=True, default='[]')

    def __str__(self):
        return f'{self.id}'
