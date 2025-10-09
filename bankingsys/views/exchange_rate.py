from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from ..models import ExchangeRate


def exchange_rate_setup(request):
    """
    Vista para configurar el tipo de cambio diario.
    Solo accesible cuando no se ha establecido el tipo de cambio de hoy.
    """
    today = date.today()
    
    # Verifica si la tasa de cambio de hoy ya existe
    existing_rate = ExchangeRate.objects.filter(date=today).first()
    
    if request.method == 'POST':
        rate_value = request.POST.get('rate')
        
        if rate_value:
            try:
                rate_value = float(rate_value)
                if rate_value <= 0:
                    messages.error(request, 'El tipo de cambio debe ser mayor que 0.')
                else:
                    # Crea o actualiza la tasa de cambio de hoy
                    ExchangeRate.objects.update_or_create(
                        date=today,
                        defaults={'rate': rate_value}
                    )
                    messages.success(request, f'Tipo de cambio del día {today} establecido correctamente: S/. {rate_value}')
                    return redirect('bankingsys:index')
            except ValueError:
                messages.error(request, 'Por favor, ingrese un valor numérico válido.')
        else:
            messages.error(request, 'Por favor, ingrese el tipo de cambio.')
    
    context = {
        'today': today,
        'existing_rate': existing_rate,
    }
    return render(request, 'bankingsys/exchange_rate/setup.html', context)
