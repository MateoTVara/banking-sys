from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from decimal import Decimal
from ..models.account import Account
from ..models.account_movement import AccountMovement
from ..models.client import Client


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

                # Registrar movimiento
                AccountMovement.objects.create(
                    account=account_to_deposit,
                    movement_type=AccountMovement.DEPOSIT,
                    amount=deposit_amount,
                    currency=account_to_deposit.currency,
                    description="Depósito en ventanilla"
                )

            messages.success(request,
                             f"¡Depósito de {deposit_amount:.2f} {account_to_deposit.currency} realizado con éxito!")
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

                # Registrar movimiento
                AccountMovement.objects.create(
                    account=account_to_withdraw,
                    movement_type=AccountMovement.WITHDRAWAL,
                    amount=-withdrawal_amount,
                    currency=account_to_withdraw.currency,
                    description="Retiro en ventanilla"
                )

            messages.success(request,
                             f"¡Retiro de {withdrawal_amount:.2f} {account_to_withdraw.currency} realizado con éxito!")
            return redirect('portal:retiro')

        except Account.DoesNotExist:
            messages.error(request, 'La cuenta seleccionada no existe o no te pertenece.')
        except Exception as e:
            if str(e) in ('Retiro de Plazos no permitido', 'Fondos insuficientes Ahorro',
                          'Fondos insuficientes Default'):
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


@login_required
def portal_transferencia(request):
    """
    Vista para transferencias entre cuentas
    """
    # Verificar que el usuario tiene un cliente asociado
    try:
        cliente_actual = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    if request.method == 'POST':
        try:
            cuenta_origen_id = request.POST.get('cuenta_origen')
            cuenta_destino_numero = request.POST.get('cuenta_destino')
            monto = request.POST.get('monto')
            descripcion = request.POST.get('descripcion', '')

            # Validaciones básicas
            if not all([cuenta_origen_id, cuenta_destino_numero, monto]):
                messages.error(request, 'Todos los campos son obligatorios')
                return redirect('portal:transferencia')

            monto = Decimal(monto)
            if monto <= 0:
                messages.error(request, 'El monto debe ser mayor a cero')
                return redirect('portal:transferencia')

            # Obtener cuentas
            cuenta_origen = get_object_or_404(Account, id=cuenta_origen_id, status=Account.Status.ACTIVE)
            cuenta_destino = get_object_or_404(Account, account_number=cuenta_destino_numero,
                                               status=Account.Status.ACTIVE)

            # Verificar que la cuenta origen pertenece al cliente
            if cuenta_origen.client != cliente_actual:
                messages.error(request, 'No tiene permisos para operar esta cuenta')
                return redirect('portal:transferencia')

            # Verificar que no sea cuenta a plazo
            if cuenta_origen.account_type == Account.AccountType.TERM:
                messages.error(request, 'No se pueden realizar transferencias desde cuentas a plazo')
                return redirect('portal:transferencia')

            # Verificar fondos
            saldo_disponible = cuenta_origen.balance
            if cuenta_origen.account_type == Account.AccountType.CURRENT:
                saldo_disponible += cuenta_origen.overdraft_limit

            if monto > saldo_disponible:
                messages.error(request, 'Fondos insuficientes')
                return redirect('portal:transferencia')

            # Verificar misma moneda
            if cuenta_origen.currency != cuenta_destino.currency:
                messages.error(request, 'Las cuentas deben ser de la misma moneda')
                return redirect('portal:transferencia')

            # Realizar transferencia
            with transaction.atomic():
                # Debitar cuenta origen
                cuenta_origen.balance -= monto
                cuenta_origen.save()

                # Acreditar cuenta destino
                cuenta_destino.balance += monto
                cuenta_destino.save()

                # Registrar movimientos
                AccountMovement.objects.create(
                    account=cuenta_origen,
                    movement_type=AccountMovement.TRANSFER,
                    amount=-monto,
                    currency=cuenta_origen.currency,
                    description=f"Transferencia a {cuenta_destino.account_number} - {descripcion}",
                    related_account=cuenta_destino
                )

                AccountMovement.objects.create(
                    account=cuenta_destino,
                    movement_type=AccountMovement.TRANSFER,
                    amount=monto,
                    currency=cuenta_destino.currency,
                    description=f"Transferencia de {cuenta_origen.account_number} - {descripcion}",
                    related_account=cuenta_origen
                )

            messages.success(request, f'Transferencia de {monto} {cuenta_origen.currency} realizada exitosamente')
            return redirect('portal:dashboard')

        except ValueError:
            messages.error(request, 'Monto inválido')
        except Exception as e:
            messages.error(request, f'Error en la transferencia: {str(e)}')

    # GET request - mostrar formulario
    cuentas_propias = Account.objects.filter(
        client=cliente_actual,
        status=Account.Status.ACTIVE
    ).exclude(account_type=Account.AccountType.TERM)  # Excluir cuentas a plazo

    return render(request, 'portal/transferencia.html', {
        'cuentas_propias': cuentas_propias,
        'client': cliente_actual
    })


@login_required
def portal_cuentas_plazo(request):
    """
    Vista para gestionar cuentas a plazo
    """
    # Verificar que el usuario tiene un cliente asociado
    try:
        cliente_actual = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    cuentas_plazo = Account.objects.filter(
        client=cliente_actual,
        account_type=Account.AccountType.TERM,
        status=Account.Status.ACTIVE
    )

    return render(request, 'portal/cuentas_plazo.html', {
        'cuentas_plazo': cuentas_plazo,
        'client': cliente_actual
    })


@login_required
def cancelar_cuenta_plazo(request, account_id):
    """
    Cancelar cuenta a plazo y depositar fondos en cuenta de ahorros
    """
    # Verificar que el usuario tiene un cliente asociado
    try:
        cliente_actual = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    try:
        cuenta_plazo = get_object_or_404(
            Account,
            id=account_id,
            client=cliente_actual,
            account_type=Account.AccountType.TERM,
            status=Account.Status.ACTIVE
        )

        with transaction.atomic():
            # Calcular intereses si aplica
            monto_final = cuenta_plazo.balance
            if cuenta_plazo.monthly_interest:
                # Cálculo simple de intereses (puedes ajustar según tu lógica)
                meses_transcurridos = (timezone.now() - cuenta_plazo.opened_at).days // 30
                if meses_transcurridos > 0:
                    interes = cuenta_plazo.balance * (cuenta_plazo.monthly_interest / 100) * meses_transcurridos
                    monto_final += interes

            # Buscar cuenta de ahorros para depositar el monto
            cuenta_ahorros = Account.objects.filter(
                client=cliente_actual,
                account_type=Account.AccountType.SAVINGS,
                status=Account.Status.ACTIVE,
                currency=cuenta_plazo.currency
            ).first()

            if not cuenta_ahorros:
                messages.error(request, 'No tiene cuenta de ahorros activa para recibir los fondos')
                return redirect('portal:cuentas_plazo')

            # Depositar en cuenta de ahorros
            cuenta_ahorros.balance += monto_final
            cuenta_ahorros.save()

            # Cerrar cuenta a plazo
            cuenta_plazo.status = Account.Status.CLOSED
            cuenta_plazo.closed_at = timezone.now()
            cuenta_plazo.save()

            # Registrar movimientos
            AccountMovement.objects.create(
                account=cuenta_plazo,
                movement_type=AccountMovement.CANCELLATION,
                amount=-cuenta_plazo.balance,
                currency=cuenta_plazo.currency,
                description="Cancelación de cuenta a plazo"
            )

            AccountMovement.objects.create(
                account=cuenta_ahorros,
                movement_type=AccountMovement.DEPOSIT,
                amount=monto_final,
                currency=cuenta_ahorros.currency,
                description=f"Depósito por cancelación de cuenta a plazo {cuenta_plazo.account_number}",
                related_account=cuenta_plazo
            )

        messages.success(request,
                         f'Cuenta a plazo cancelada exitosamente. Se depositaron {monto_final} {cuenta_plazo.currency} en su cuenta de ahorros')
        return redirect('portal:cuentas_plazo')

    except Exception as e:
        messages.error(request, f'Error al cancelar la cuenta a plazo: {str(e)}')
        return redirect('portal:cuentas_plazo')


@login_required
def renovar_cuenta_plazo(request, account_id):
    """
    Renovar cuenta a plazo capitalizando intereses
    """
    # Verificar que el usuario tiene un cliente asociado
    try:
        cliente_actual = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    try:
        cuenta_plazo = get_object_or_404(
            Account,
            id=account_id,
            client=cliente_actual,
            account_type=Account.AccountType.TERM,
            status=Account.Status.ACTIVE
        )

        with transaction.atomic():
            # Calcular intereses y renovar
            monto_renovado = cuenta_plazo.balance
            if cuenta_plazo.monthly_interest:
                meses_transcurridos = (timezone.now() - cuenta_plazo.opened_at).days // 30
                if meses_transcurridos > 0:
                    interes = cuenta_plazo.balance * (cuenta_plazo.monthly_interest / 100) * meses_transcurridos
                    monto_renovado += interes

            # Actualizar cuenta con nuevo monto y fecha
            cuenta_plazo.balance = monto_renovado
            cuenta_plazo.opened_at = timezone.now()
            cuenta_plazo.save()

            # Registrar movimiento de renovación
            AccountMovement.objects.create(
                account=cuenta_plazo,
                movement_type=AccountMovement.RENEWAL,
                amount=monto_renovado,
                currency=cuenta_plazo.currency,
                description="Renovación de cuenta a plazo"
            )

        messages.success(request,
                         f'Cuenta a plazo renovada exitosamente. Nuevo balance: {monto_renovado} {cuenta_plazo.currency}')
        return redirect('portal:cuentas_plazo')

    except Exception as e:
        messages.error(request, f'Error al renovar la cuenta a plazo: {str(e)}')
        return redirect('portal:cuentas_plazo')


@login_required
def apertura_cuenta(request):
    """
    Vista para la apertura de cuentas (Ahorros, Corriente, Plazo Fijo).
    Los clientes pueden abrir cuentas únicamente a su nombre.
    
    Reglas de negocio:
    - Cuentas de ahorro y corriente: pueden abrirse con saldo cero, en soles o dólares
    - Cuentas a plazo: requieren monto inicial, plazo de permanencia e interés mensual
    """
    try:
        client = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    if request.method == 'POST':
        try:
            account_type = request.POST.get('account_type')
            currency = request.POST.get('currency')
            initial_amount_str = request.POST.get('initial_amount', '0')
            
            # Validaciones básicas
            if not account_type or not currency:
                messages.error(request, 'Debe seleccionar el tipo de cuenta y la moneda.')
                return redirect('portal:apertura_cuenta')
            
            # Validar tipo de cuenta
            if account_type not in [Account.AccountType.SAVINGS, Account.AccountType.CURRENT, Account.AccountType.TERM]:
                messages.error(request, 'Tipo de cuenta inválido.')
                return redirect('portal:apertura_cuenta')
            
            # Validar moneda
            if currency not in [Account.Currency.PEN, Account.Currency.USD]:
                messages.error(request, 'Moneda inválida.')
                return redirect('portal:apertura_cuenta')
            
            # Validar monto inicial
            try:
                initial_amount = Decimal(initial_amount_str) if initial_amount_str else Decimal('0')
            except:
                messages.error(request, 'El monto inicial no es válido.')
                return redirect('portal:apertura_cuenta')
            
            if initial_amount < 0:
                messages.error(request, 'El monto inicial no puede ser negativo.')
                return redirect('portal:apertura_cuenta')
            
            with transaction.atomic():
                # Crear la nueva cuenta
                nueva_cuenta = Account(
                    client=client,
                    account_type=account_type,
                    currency=currency,
                    balance=initial_amount,
                    status=Account.Status.ACTIVE
                )
                
                # Para cuentas a plazo, validar campos adicionales
                if account_type == Account.AccountType.TERM:
                    term_months_str = request.POST.get('term_months')
                    monthly_interest_str = request.POST.get('monthly_interest')
                    
                    # Validar que se ingresaron los campos requeridos
                    if not term_months_str or not monthly_interest_str:
                        messages.error(request, 'Para cuentas a plazo debe especificar el plazo en meses y el interés mensual.')
                        return redirect('portal:apertura_cuenta')
                    
                    # Validar que el monto inicial no sea cero
                    if initial_amount <= 0:
                        messages.error(request, 'Las cuentas a plazo deben abrirse con un monto inicial mayor a cero.')
                        return redirect('portal:apertura_cuenta')
                    
                    try:
                        term_months = int(term_months_str)
                        monthly_interest = Decimal(monthly_interest_str)
                    except:
                        messages.error(request, 'El plazo en meses o el interés mensual no son válidos.')
                        return redirect('portal:apertura_cuenta')
                    
                    if term_months <= 0:
                        messages.error(request, 'El plazo en meses debe ser mayor a cero.')
                        return redirect('portal:apertura_cuenta')
                    
                    if monthly_interest < 0:
                        messages.error(request, 'El interés mensual no puede ser negativo.')
                        return redirect('portal:apertura_cuenta')
                    
                    nueva_cuenta.term_months = term_months
                    nueva_cuenta.monthly_interest = monthly_interest
                
                # Guardar la cuenta
                nueva_cuenta.save()
                
                # Registrar movimiento inicial si hay monto
                if initial_amount > 0:
                    AccountMovement.objects.create(
                        account=nueva_cuenta,
                        movement_type=AccountMovement.DEPOSIT,
                        amount=initial_amount,
                        currency=currency,
                        description="Depósito inicial por apertura de cuenta"
                    )
                
                # Mensaje de éxito según el tipo de cuenta
                account_type_label = dict(Account.AccountType.choices)[account_type]
                messages.success(
                    request,
                    f'¡Cuenta de {account_type_label} abierta exitosamente! Número de cuenta: {nueva_cuenta.account_number}'
                )
                return redirect('portal:apertura_cuenta')
        
        except Exception as e:
            messages.error(request, f'Ocurrió un error al abrir la cuenta: {str(e)}')
            return redirect('portal:apertura_cuenta')
    
    # GET request - mostrar formulario
    context = {
        'client': client,
        'account_types': Account.AccountType.choices,
        'currencies': Account.Currency.choices,
    }
    return render(request, 'portal/cuenta/apertura.html', context)


@login_required
def cierre_cuenta(request):
    """
    Vista para el cierre de cuentas del cliente.
    
    Regla de negocio:
    - Solo se pueden cerrar cuentas con saldo cero
    """
    try:
        client = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')
    
    if request.method == 'POST':
        try:
            account_id = request.POST.get('account_id')
            
            if not account_id:
                messages.error(request, 'Debe seleccionar una cuenta.')
                return redirect('portal:cierre_cuenta')
            
            with transaction.atomic():
                # Obtener la cuenta del cliente
                cuenta = Account.objects.select_for_update().get(
                    id=account_id,
                    client=client,
                    status=Account.Status.ACTIVE
                )
                
                # Validar que el saldo sea cero
                if cuenta.balance != 0:
                    messages.error(
                        request,
                        f'No se puede cerrar la cuenta {cuenta.account_number}. '
                        f'La cuenta debe tener saldo cero. Saldo actual: {cuenta.balance} {cuenta.currency}'
                    )
                    return redirect('portal:cierre_cuenta')
                
                # Cambiar el estado de la cuenta a CLOSED
                cuenta.status = Account.Status.CLOSED
                cuenta.save()
                
                # Registrar movimiento de cierre
                AccountMovement.objects.create(
                    account=cuenta,
                    movement_type=AccountMovement.CLOSURE,
                    amount=Decimal('0'),
                    currency=cuenta.currency,
                    description="Cierre de cuenta"
                )
                
                account_type_label = dict(Account.AccountType.choices)[cuenta.account_type]
                messages.success(
                    request,
                    f'La cuenta {cuenta.account_number} ({account_type_label}) ha sido cerrada exitosamente.'
                )
                return redirect('portal:cierre_cuenta')
        
        except Account.DoesNotExist:
            messages.error(request, 'La cuenta seleccionada no existe, no te pertenece o ya está cerrada.')
            return redirect('portal:cierre_cuenta')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al cerrar la cuenta: {str(e)}')
            return redirect('portal:cierre_cuenta')
    
    # GET request - mostrar lista de cuentas activas
    cuentas_activas = Account.objects.filter(
        client=client,
        status=Account.Status.ACTIVE
    ).order_by('-opened_at')
    
    context = {
        'client': client,
        'cuentas': cuentas_activas,
    }
    return render(request, 'portal/cuenta/cierre.html', context)


@login_required
def mis_cuentas(request):
    """
    Vista para mostrar todas las cuentas del cliente (activas e inactivas).
    """
    try:
        client = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')
    
    # Obtener todas las cuentas del cliente
    cuentas = Account.objects.filter(client=client).order_by('-opened_at')
    
    # Calcular totales por moneda (solo cuentas activas)
    cuentas_activas = cuentas.filter(status=Account.Status.ACTIVE)
    total_pen = sum(acc.balance for acc in cuentas_activas if acc.currency == Account.Currency.PEN)
    total_usd = sum(acc.balance for acc in cuentas_activas if acc.currency == Account.Currency.USD)
    
    context = {
        'client': client,
        'cuentas': cuentas,
        'total_pen': total_pen,
        'total_usd': total_usd,
    }
    return render(request, 'portal/cuenta/mis_cuentas.html', context)


@login_required
def mis_movimientos(request):
    """
    Vista para mostrar los últimos 20 movimientos del cliente a través de todas sus cuentas
    """
    # Verificar que el usuario pertenece al grupo 'clients'
    if not request.user.groups.filter(name='clients').exists():
        messages.error(request, 'No tienes acceso a esta sección.')
        return redirect('bankingsys:index')

    # Verificar que el usuario tiene un cliente asociado
    try:
        client = request.user.client
    except Exception as e:
        messages.error(request, 'Tu usuario no tiene un cliente asociado.')
        return redirect('login')

    # Obtener todas las cuentas del cliente
    cuentas = Account.objects.filter(client=client)
    
    # Obtener los últimos 20 movimientos de todas las cuentas del cliente
    movimientos = AccountMovement.objects.filter(
        account__in=cuentas
    ).select_related('account', 'related_account').order_by('-created_at')[:20]
    
    context = {
        'client': client,
        'movimientos': movimientos,
    }
    return render(request, 'portal/movimientos.html', context)