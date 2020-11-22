from django.db import models


class CooksOrders(models.Model):
    orders = models.TextField(null=True, default='[]')

    def __str__(self):
        return f'{self.id}'


class DistributionOrders(models.Model):
    orders = models.TextField(null=True, default='[]')

    def __str__(self):
        return f'{self.id}'
