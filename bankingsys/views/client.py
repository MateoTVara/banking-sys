from django.shortcuts import render
from ..models import Client


def client_list(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'bankingsys/client/clients.html', context)

def client_register(request):
    return render(request, 'bankingsys/client/register.html')