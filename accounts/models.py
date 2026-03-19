from django.contrib.auth.models import AbstractUser
from django.db import models


class FindPostcodeUser(AbstractUser):
    comms_preferences = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}-({self.username})'


class ApiKeys(models.Model):
    project = models.CharField(max_length=100)
    api_key_hash = models.CharField(max_length=64, unique=True, db_index=True)
    owner = models.ForeignKey(
        FindPostcodeUser,
        on_delete=models.CASCADE
    )
