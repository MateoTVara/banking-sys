from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    failed_attempts = models.IntegerField(default=0)
