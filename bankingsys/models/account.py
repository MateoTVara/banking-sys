from django.db import models
from .client import Client


class Account(models.Model):
    class AccountType(models.TextChoices):
        SAVINGS = 'savings', 'Ahorros'
        CURRENT = 'current', 'Corriente'
        TERM = 'term', 'Plazos'

    class Currency(models.TextChoices):
        PEN = 'PEN', 'Soles'
        USD = 'USD', 'Dólares'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Activo'
        INACTIVE = 'inactive', 'Inactiva'
        CLOSED = 'closed', 'Cerrada'

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=AccountType.choices)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    overdraft_limit = models.DecimalField(max_digits=14, decimal_places=2, default=0)  # Para cuentas corrientes
    term_months = models.IntegerField(blank=True, null=True)  # Para cuentas a plazo
    monthly_interest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Para cuentas a plazo
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.account_number} - {self.client.code} - {self.account_type} - {self.currency}"
