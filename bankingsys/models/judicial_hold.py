from django.db import models
from .account import Account


class JudicialHold(models.Model):
    PARTIAL = 'partial'
    TOTAL = 'total'
    HOLD_TYPE_CHOICES = [
        (PARTIAL, 'Parcial'),
        (TOTAL, 'Total'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    hold_type = models.CharField(max_length=10, choices=HOLD_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)  # Para retenciones parciales
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.account} - {self.hold_type} - {'Active' if self.is_active else 'Removed'}"
