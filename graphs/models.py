from django.conf import settings
from django.db import models


class DishesByPopularity(models.Model):
    number_of_orders = models.CharField(max_length=1000)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Dishes By Popularity'

    def __str__(self):
        return f'{self.datetime}'


class EmployeeWorkingHours(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number_of_orders = models.IntegerField(default=1)
    datetime = models.DateTimeField(blank=True)

    @classmethod
    def create(cls, user):
        instance = cls(user=user)
        return instance

    class Meta:
        verbose_name_plural = 'Employee Orders Done'

    def __str__(self):
        return f'{self.datetime}'
