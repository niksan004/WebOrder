from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    is_cook = models.BooleanField(default=False)
    is_distributor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
