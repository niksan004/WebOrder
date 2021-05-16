from django.db import models


class CooksOrders(models.Model):
    orders = models.TextField(null=True, default='[]')

    class Meta:
        verbose_name_plural = 'Cooks orders'

    def __str__(self):
        return f'{self.id}'


class DistributionOrders(models.Model):
    orders = models.TextField(null=True, default='[]')

    class Meta:
        verbose_name_plural = 'Distribution orders'

    def __str__(self):
        return f'{self.id}'
