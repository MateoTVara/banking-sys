from django.shortcuts import render
from ..models import Account


def account_list(request):
    accounts = Account.objects.all()
    context = {
        'accounts': accounts
    }
    return render(request, 'bankingsys/account/accounts.html', context)
