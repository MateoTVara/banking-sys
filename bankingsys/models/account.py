from django.db import models
from django.utils import timezone
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
    account_type = models.CharField(max_length=10, choices=AccountType.choices, blank=False, default=AccountType.SAVINGS)
    currency = models.CharField(max_length=3, choices=Currency.choices, blank=False, default=Currency.PEN)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    overdraft_limit = models.DecimalField(max_digits=14, decimal_places=2, default=0)  # Para cuentas corrientes
    term_months = models.IntegerField(blank=True, null=True)  # Para cuentas a plazo
    monthly_interest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Para cuentas a plazo
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.account_number} - {self.client.code} - {self.account_type} - {self.currency}"

    @staticmethod
    def generate_account_number(currency, account_type):
        prefix = "191"
        # Get next sequential number (count + 1)
        next_number = Account.objects.count() + 1
        number_str = f"{next_number:08d}"
        # Y: 0 for PEN, 1 for USD
        y = "0" if currency == Account.Currency.PEN else "1"
        # X: 1 for savings, 2 for current, 3 for term
        if account_type == Account.AccountType.SAVINGS:
            x = "1"
        elif account_type == Account.AccountType.CURRENT:
            x = "2"
        elif account_type == Account.AccountType.TERM:
            x = "3"
        else:
            x = "0"
        return f"{prefix}-{number_str}-{y}-0{x}"

    def save(self, *args, **kwargs):
        # Generate account number only when creating a new account
        if not self.pk and not self.account_number:
            self.account_number = Account.generate_account_number(self.currency, self.account_type)

        # Obtiene el estado previo para verificar cambios
        if self.pk:
            prev = Account.objects.get(pk=self.pk)
            prev_status = prev.status
        else:
            prev_status = None

        # Solo se establece closed_at si el estado cambió a CLOSED
        if self.status == self.Status.CLOSED and prev_status != self.Status.CLOSED:
            self.closed_at = timezone.now()
        elif self.status != self.Status.CLOSED:
            self.closed_at = None

        # Ajusta campos según el tipo de cuenta
        if self.account_type != self.AccountType.CURRENT:
            self.overdraft_limit = 0
        
        # Las cuentas que no son a plazo no deben tener term_months ni monthly_interest
        if self.account_type != self.AccountType.TERM:
            self.term_months = None
            self.monthly_interest = None

        super().save(*args, **kwargs)
