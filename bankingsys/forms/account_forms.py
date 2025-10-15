from django import forms
from ..models import Account, Client


class AccountOpeningForm(forms.ModelForm):
    ACCOUNT_TYPES = [
        ('savings', 'Cuenta de Ahorro'),
        ('current', 'Cuenta Corriente'),
        ('term', 'Cuenta a Plazos'),
    ]

    CURRENCIES = [
        ('PEN', 'Soles (PEN)'),
        ('USD', 'Dólares (USD)'),
    ]

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Cliente",
        empty_label="Seleccione un cliente"
    )

    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPES,
        label="Tipo de Cuenta"
    )

    currency = forms.ChoiceField(
        choices=CURRENCIES,
        label="Moneda"
    )

    initial_deposit = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label="Depósito Inicial",
        min_value=0.00
    )

    # Campos específicos para cuenta corriente
    overdraft_limit = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label="Límite de Sobregiro",
        required=False,
        initial=0.00
    )

    # Campos específicos para cuenta a plazos
    term_months = forms.IntegerField(
        label="Plazo (meses)",
        required=False,
        min_value=1,
        max_value=60
    )

    monthly_interest = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Tasa de Interés Mensual (%)",
        required=False,
        initial=0.00
    )

    class Meta:
        model = Account
        fields = ['client', 'account_type', 'currency', 'initial_deposit']

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')
        overdraft_limit = cleaned_data.get('overdraft_limit', 0)
        term_months = cleaned_data.get('term_months')
        monthly_interest = cleaned_data.get('monthly_interest')
        initial_deposit = cleaned_data.get('initial_deposit', 0)

        # Validaciones específicas por tipo de cuenta
        if account_type == 'current' and overdraft_limit < 0:
            raise forms.ValidationError("El límite de sobregiro no puede ser negativo")

        if account_type == 'term':
            if not term_months:
                raise forms.ValidationError("Para cuenta a plazos debe especificar el plazo")
            if not monthly_interest:
                raise forms.ValidationError("Para cuenta a plazos debe especificar la tasa de interés")
            if initial_deposit < 1000:  # Depósito mínimo para cuenta a plazos
                raise forms.ValidationError("La cuenta a plazos requiere un depósito mínimo de 1000")

        if account_type == 'savings' and initial_deposit < 10:  # Depósito mínimo para ahorros
            raise forms.ValidationError("La cuenta de ahorros requiere un depósito mínimo de 10")

        return cleaned_data