from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages  # <-- Añade esto
from ..models import Account, Client

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['status']

class AccountOpeningForm(forms.ModelForm):
    initial_deposit = forms.DecimalField(label="Depósito Inicial", min_value=0, required=True)

    class Meta:
        model = Account
        fields = [
            'client', 'account_type', 'currency', 'overdraft_limit',
            'term_months', 'monthly_interest'
        ]

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')
        initial_deposit = cleaned_data.get('initial_deposit')

        # Validaciones según tipo de cuenta
        if account_type == Account.AccountType.SAVINGS and initial_deposit < 10:
            self.add_error('initial_deposit', "El depósito inicial mínimo para cuenta de ahorro es S/ 10.")
        elif account_type == Account.AccountType.CURRENT and initial_deposit < 100:
            self.add_error('initial_deposit', "El depósito inicial mínimo para cuenta corriente es S/ 100.")
        elif account_type == Account.AccountType.TERM and initial_deposit < 1000:
            self.add_error('initial_deposit', "El depósito inicial mínimo para cuenta a plazos es S/ 1000.")

        return cleaned_data

def account_edit(request):
    account_id = request.POST.get('account') or request.GET.get('account')
    if not account_id:
        return redirect('bankingsys:accounts')
    try:
        account = Account.objects.get(pk=account_id)
    except Account.DoesNotExist:
        return redirect('bankingsys:accounts')
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            if new_status in [Account.Status.INACTIVE, Account.Status.CLOSED] and account.balance > 0:
                messages.error(request, "No se puede inactivar ni cerrar la cuenta mientras tenga saldo.")
            else:
                form.save()
                return redirect('bankingsys:account_register')
    else:
        form = AccountForm(instance=account)
    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'bankingsys/account/account_edit.html', context)

def account_register(request):
    accounts = Account.objects.all()

    if request.method == 'POST':
        form = AccountOpeningForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.balance = form.cleaned_data['initial_deposit']
            account.save()
            return redirect('bankingsys:account_register')
    else:
        form = AccountOpeningForm()

    context = {
        'form': form,
        'accounts': accounts,
    }
    return render(request, 'bankingsys/account/register.html', context)

def account_list(request):
    accounts = Account.objects.all()
    context = {
        'accounts': accounts
    }
    return render(request, 'bankingsys/account/accounts.html', context)
