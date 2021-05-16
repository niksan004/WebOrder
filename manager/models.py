from django.db import models


class PaidTable(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    bill = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.datetime}'
