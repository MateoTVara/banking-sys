from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from decimal import Decimal
from ..models import JudicialHold, Client, Account, ExchangeRate


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

def judicial_hold_register_form(request):
    if request.method == 'POST':
        account_id = request.POST.get('account')
        hold_type = request.POST.get('hold_type')
        hold_amount = request.POST.get('hold_amount')
        
        # Obtener la cuenta
        account = get_object_or_404(Account, id=account_id)
        
        # Si no se proporciona hold_type, significa que es la visualización inicial del formulario
        # (viene de la página de selección de cuenta)
        if not hold_type:
            context = {
                'account': account,
                'hold_type_choices': JudicialHold.HOLD_TYPE_CHOICES
            }
            return render(request, 'bankingsys/judicial_hold/register_form.html', context)
        
        # Validación 1: Verificar si la cuenta ya tiene un embargo judicial activo
        existing_hold = JudicialHold.objects.filter(account=account, is_active=True).first()
        if existing_hold:
            messages.error(request, f'La cuenta {account.account_number} ya tiene un embargo activo.')
            context = {
                'account': account,
                'hold_type_choices': JudicialHold.HOLD_TYPE_CHOICES
            }
            return render(request, 'bankingsys/judicial_hold/register_form.html', context)
        
        # Calcular el saldo de la cuenta en PEN para la validación
        balance_in_pen = account.balance
        if account.currency == 'USD':
            # Obtener el tipo de cambio de hoy
            today = date.today()
            try:
                exchange_rate = ExchangeRate.objects.get(date=today)
                balance_in_pen = account.balance * exchange_rate.rate
            except ExchangeRate.DoesNotExist:
                messages.error(request, f'No se ha configurado el tipo de cambio para el día {today}. Por favor, configure el tipo de cambio antes de continuar.')
                context = {
                    'account': account,
                    'hold_type_choices': JudicialHold.HOLD_TYPE_CHOICES
                }
                return render(request, 'bankingsys/judicial_hold/register_form.html', context)
        
        # Validación 2: Para embargos parciales, validar el monto
        if hold_type == JudicialHold.PARTIAL:
            if not hold_amount:
                messages.error(request, 'Debe ingresar el monto para un embargo parcial.')
                context = {
                    'account': account,
                    'hold_type_choices': JudicialHold.HOLD_TYPE_CHOICES
                }
                return render(request, 'bankingsys/judicial_hold/register_form.html', context)
            
            try:
                hold_amount_decimal = Decimal(hold_amount)
                if hold_amount_decimal <= 0:
                    messages.error(request, 'El monto del embargo debe ser mayor que 0.')
                    context = {
                        'account': account,
                        'hold_type_choices': JudicialHold.HOLD_TYPE_CHOICES
                    }
                    return render(request, 'bankingsys/judicial_hold/register_form.html', context)
                
                # Verificar si el monto del embargo excede el saldo (en PEN)
                if hold_amount_decimal > balance_in_pen:
                    messages.error(request, f'El monto del embargo (S/. {hold_amount_decimal}) no puede ser mayor que el saldo de la cuenta (S/. {balance_in_pen:.2f}).')
                    context = {
                        'account': account,
                        'hold_type_choices': JudicialHold.HOLD_TYPE_CHOICES
                    }
                    return render(request, 'bankingsys/judicial_hold/register_form.html', context)
                
            except (ValueError, TypeError):
                messages.error(request, 'Por favor, ingrese un monto válido.')
                context = {
                    'account': account,
                    'hold_type_choices': JudicialHold.HOLD_TYPE_CHOICES
                }
                return render(request, 'bankingsys/judicial_hold/register_form.html', context)
        else:
            # Para embargos totales, establecer el monto en 0
            hold_amount_decimal = Decimal('0')
        
        # Crear el embargo judicial
        judicial_hold = JudicialHold.objects.create(
            account=account,
            hold_type=hold_type,
            amount=hold_amount_decimal,
            is_active=True
        )
        
        hold_type_display = 'total' if hold_type == JudicialHold.TOTAL else 'parcial'
        amount_info = f' por S/. {hold_amount_decimal}' if hold_type == JudicialHold.PARTIAL else ''
        messages.success(request, f'Embargo {hold_type_display}{amount_info} registrado exitosamente para la cuenta {account.account_number}.')
        
        return redirect('bankingsys:judicial_hold_register')
    
    # Si es una solicitud GET (no debería ocurrir, pero redirigir por si acaso)
    return redirect('bankingsys:judicial_hold_register')