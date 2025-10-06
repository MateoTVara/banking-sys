from django.db import models
from .account import Account


class AccountMovement(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'
    RENEWAL = 'renewal'
    CANCELLATION = 'cancellation'
    MOVEMENT_TYPE_CHOICES = [
        (DEPOSIT, 'Depósito'),
        (WITHDRAWAL, 'Retiro'),
        (TRANSFER, 'Transferencia'),
        (RENEWAL, 'Renovación'),
        (CANCELLATION, 'Cancelación'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=15, choices=MOVEMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Account.Currency.choices)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, related_name='related_movements')
    authorized_key = models.CharField(max_length=50, blank=True, null=True)  # Para depositos > S/2000
    origin_of_funds = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.account} - {self.movement_type} - {self.amount} {self.currency}"
