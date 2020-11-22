from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    COOK = 1
    DISTRIBUTOR = 2
    MANAGER = 3

    ROLE_CHOICES = (
      (COOK, 'cook'),
      (DISTRIBUTOR, 'distributor'),
      (MANAGER, 'manager'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
