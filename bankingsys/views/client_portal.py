from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Account


def portal_dashboard(request):
    """
    Dashboard principal para clientes del grupo 'clients'
    """
    # Verificar que el usuario pertenece al grupo 'clients'
    if not request.user.groups.filter(name='clients').exists():
        messages.error(request, 'No tienes acceso a esta sección.')
        return redirect('bankingsys:index')
    
    # Verificar que el usuario tiene un cliente asociado
    if not request.user.client:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')
    
    client = request.user.client
    # accounts = Account.objects.filter(client=client)
    
    # Calcular totales por moneda
    # total_pen = sum(acc.balance for acc in accounts if acc.currency == Account.Currency.PEN)
    # total_usd = sum(acc.balance for acc in accounts if acc.currency == Account.Currency.USD)
    
    context = {
        'client': client,
        # 'accounts': accounts,
        # 'total_pen': total_pen,
        # 'total_usd': total_usd,
    }
    return render(request, 'portal/dashboard.html', context)
