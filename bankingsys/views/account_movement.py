from django.shortcuts import render
from ..models import AccountMovement


def account_movement_list(request):
    account_movements = AccountMovement.objects.all()
    context = {
        'account_movements': account_movements
    }
    return render(request, 'bankingsys/account_movement/account_movements.html', context)
