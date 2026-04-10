from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import FindPostcodeUserManager


class FindPostcodeUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}-({self.username})'


    objects = FindPostcodeUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
