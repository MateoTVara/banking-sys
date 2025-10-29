from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Account
from django.contrib.auth.decorators import login_required
from decimal import Decimal 
from django.db.models import F 
from django.db import transaction 


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
@login_required
def portal_deposito(request):
    """
    Vista para la página de depósitos del cliente.
    Maneja GET (mostrar) y POST (procesar depósito).
    """
    
    # 1. Obtener el cliente (lo hacemos al inicio)
    try:
        client = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    # 2. Lógica para cuando se envía el formulario (POST)
    if request.method == 'POST':
        try:
            account_id = request.POST.get('account_id')
            amount_str = request.POST.get('amount')

            # Validación 1: Campos vacíos
            if not account_id or not amount_str:
                messages.error(request, 'Debe seleccionar una cuenta y un monto.')
                return redirect('portal:deposito')

            # Validación 2: Monto válido (usamos Decimal para precisión)
            try:
                deposit_amount = Decimal(amount_str)
            except:
                messages.error(request, 'El monto ingresado no es válido.')
                return redirect('portal:deposito')
            
            # Validación 3: Monto positivo
            if deposit_amount <= 0:
                messages.error(request, 'El monto a depositar debe ser positivo.')
                return redirect('portal:deposito')

            # --- Inicio de la Transacción ---
            with transaction.atomic():
                
                # Obtenemos la cuenta de forma segura
                account_to_deposit = Account.objects.select_for_update().get(id=account_id, client=client)

                # REGLA: No se puede depositar en Cuentas a Plazo
                if account_to_deposit.account_type == Account.AccountType.TERM:
                    messages.error(request, 'No se pueden realizar depósitos a cuentas de Plazo Fijo.')
                    return redirect('portal:deposito')

                # Si es Ahorro o Corriente, procede con el depósito
                account_to_deposit.balance = F('balance') + deposit_amount
                account_to_deposit.save()
            messages.success(request, f"¡Depósito de S/ {deposit_amount:.2f} realizado con éxito!")
            return redirect('portal:deposito')

        except Account.DoesNotExist:
            messages.error(request, 'La cuenta seleccionada no existe o no te pertenece.')
        except Exception as e:
            # Captura cualquier otro error
            messages.error(request, f'Ocurrió un error inesperado: {e}')
        
        # Si algo falló, redirigimos de todas formas
        return redirect('portal:deposito')

    # 3. Lógica para cargar la página (GET)
    accounts = Account.objects.filter(client=client)
    
    context = {
        'client': client,
        'accounts': accounts
    }
    
    return render(request, 'portal/client_depo/deposito.html', context)

@login_required
def portal_retiro(request):
    """
    Vista para la página de retiros del cliente.
    Incluye lógica de negocio por tipo de cuenta.
    """
    
    try:
        client = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    if request.method == 'POST':
        try:
            account_id = request.POST.get('account_id')
            amount_str = request.POST.get('amount')

            if not account_id or not amount_str:
                messages.error(request, 'Debe seleccionar una cuenta y un monto.')
                return redirect('portal:retiro')
            try:
                withdrawal_amount = Decimal(amount_str)
            except:
                messages.error(request, 'El monto ingresado no es válido.')
                return redirect('portal:retiro')
            if withdrawal_amount <= 0:
                messages.error(request, 'El monto a retirar debe ser positivo.')
                return redirect('portal:retiro')

            # --- INICIO DE LA LÓGICA DE NEGOCIO ---
            with transaction.atomic():
                account_to_withdraw = Account.objects.select_for_update().get(id=account_id, client=client)
                
                # REGLA 1: CUENTA A PLAZOS (No se puede retirar)
                if account_to_withdraw.account_type == 'term':
                    messages.error(request, 'No se pueden realizar retiros de Cuentas a Plazos.')
                    raise Exception('Retiro de Plazos no permitido')

                # REGLA 2: CUENTA DE AHORRO (No puede sobregirarse)
                elif account_to_withdraw.account_type == 'savings':
                    if withdrawal_amount > account_to_withdraw.balance:
                        messages.error(request, 'Fondos insuficientes. Las cuentas de Ahorro no pueden sobregirarse.')
                        raise Exception('Fondos insuficientes Ahorro')
                
                # REGLA 3: CUENTA CORRIENTE (Sí puede sobregirarse)
                elif account_to_withdraw.account_type == 'current':
                    pass
                else:
                    # Aplicamos la regla más segura (no sobregirar)
                    if withdrawal_amount > account_to_withdraw.balance:
                        messages.error(request, 'Fondos insuficientes para este tipo de cuenta.')
                        raise Exception('Fondos insuficientes Default')

                # Si pasó todas las reglas, se ejecuta la resta:
                account_to_withdraw.balance = F('balance') - withdrawal_amount
                account_to_withdraw.save()
            
            messages.success(request, f"¡Retiro de S/ {withdrawal_amount:.2f} realizado con éxito!")
            return redirect('portal:retiro')

        except Account.DoesNotExist:
            messages.error(request, 'La cuenta seleccionada no existe o no te pertenece.')
        except Exception as e:
            if str(e) in ('Retiro de Plazos no permitido', 'Fondos insuficientes Ahorro', 'Fondos insuficientes Default'):
                pass
            else:
                messages.error(request, f'Ocurrió un error inesperado: {e}')
        
        return redirect('portal:retiro')

    accounts = Account.objects.filter(client=client)
    context = {
        'client': client,
        'accounts': accounts
    }
    return render(request, 'portal/client_depo/retiro.html', context)
