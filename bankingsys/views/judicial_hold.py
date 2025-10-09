from django.shortcuts import render
from ..models import JudicialHold, Client, Account


def judicial_hold_list(request):
    judicial_holds = JudicialHold.objects.all()
    context = {
        'judicial_holds': judicial_holds
    }
    return render(request, 'bankingsys/judicial_hold/judicial_holds.html', context)


def judicial_hold_register(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'bankingsys/judicial_hold/register.html', context)