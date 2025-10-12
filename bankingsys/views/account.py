from django.shortcuts import render, get_object_or_404, redirect
from ..models import Account
from django import forms

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['status']

def account_edit(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('bankingsys:accounts')
    else:
        form = AccountForm(instance=account)
    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'bankingsys/account/account_edit.html', context)

def account_list(request):
    accounts = Account.objects.all()
    context = {
        'accounts': accounts
    }
    return render(request, 'bankingsys/account/accounts.html', context)
