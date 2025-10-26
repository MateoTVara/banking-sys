from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    failed_attempts = models.IntegerField(default=0)
    client = models.OneToOneField(
        'bankingsys.Client',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Only for users in the 'client' group"
    )