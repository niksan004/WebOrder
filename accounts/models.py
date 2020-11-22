from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_cook = models.BooleanField('cook status', default=False)
    is_distributor = models.BooleanField('distributor status', default=False)
    is_manager = models.BooleanField('manager status', default=False)


class Cook(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Distributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
