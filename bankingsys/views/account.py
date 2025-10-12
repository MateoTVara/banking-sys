from django.shortcuts import render, redirect
from django.http import Http404
from ..models import Account
from django import forms

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['status']

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
