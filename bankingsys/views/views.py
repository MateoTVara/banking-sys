from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Account, Client, AccountMovement
from .forms.account_forms import AccountOpeningForm

@login_required
def account_opening(request):
    """Vista para apertura de nuevas cuentas"""
    if request.method == 'POST':
        form = AccountOpeningForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Generar número de cuenta automáticamente
                    last_account = Account.objects.order_by('-id').first()
                    if last_account and last_account.account_number:
                        try:
                            last_number = int(last_account.account_number.split('-')[1])
                            next_number = last_number + 1
                        except (ValueError, IndexError):
                            next_number = 1
                    else:
                        next_number = 1

                    currency_suffix = '02' if form.cleaned_data['currency'] == 'USD' else '01'
                    account_number = f"191-{next_number:08d}-0-{currency_suffix}"

                    # Crear la cuenta
                    account = Account(
                        client=form.cleaned_data['client'],
                        account_number=account_number,
                        account_type=form.cleaned_data['account_type'],
                        currency=form.cleaned_data['currency'],
                        balance=form.cleaned_data['initial_deposit'],
                        status='active'
                    )

                    # Campos específicos por tipo de cuenta
                    if form.cleaned_data['account_type'] == 'current':
                        account.overdraft_limit = form.cleaned_data['overdraft_limit'] or 0

                    if form.cleaned_data['account_type'] == 'term':
                        account.term_months = form.cleaned_data['term_months']
                        account.monthly_interest = form.cleaned_data['monthly_interest']

                    account.save()

                    # Crear movimiento por el depósito inicial
                    if form.cleaned_data['initial_deposit'] > 0:
                        AccountMovement.objects.create(
                            account=account,
                            movement_type='deposit',
                            amount=form.cleaned_data['initial_deposit'],
                            currency=form.cleaned_data['currency'],
                            description='Depósito inicial - Apertura de cuenta',
                            origin_of_funds='Fondos propios'
                        )

                    messages.success(request, f'✅ Cuenta creada exitosamente! Número: {account_number}')
                    return redirect('bankingsys:account_list')

            except Exception as e:
                messages.error(request, f'❌ Error al crear la cuenta: {str(e)}')
    else:
        form = AccountOpeningForm()

    return render(request, 'bankingsys/account_opening.html', {'form': form})

@login_required
def account_list(request):
    """Vista para listar todas las cuentas"""
    accounts = Account.objects.select_related('client').all()
    return render(request, 'bankingsys/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, account_id):
    """Vista para ver detalle de una cuenta específica"""
    account = get_object_or_404(Account, id=account_id)
    movements = AccountMovement.objects.filter(account=account).order_by('-created_at')
    return render(request, 'bankingsys/account_detail.html', {
        'account': account,
        'movements': movements
    })