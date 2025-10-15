from django.shortcuts import render
from django.db.models import Count
from bankingsys.models.client import Client
from bankingsys.models.account import Account
from bankingsys.models.judicial_hold import JudicialHold
from bankingsys.models.account_movement import AccountMovement
from datetime import datetime


def index(request):
    # Obtener conteos por tipo de movimiento
    movement_types = dict(AccountMovement.MOVEMENT_TYPE_CHOICES)
    movement_counts = {
        key: AccountMovement.objects.filter(movement_type=key).count()
        for key in movement_types.keys()
    }

    # Agrega movimientos por fecha
    movements_by_date = (
        AccountMovement.objects
        .values('created_at__date')
        .annotate(count=Count('id'))
        .order_by('created_at__date')
    )
    movement_dates = [
        datetime.strptime(str(m['created_at__date']), "%Y-%m-%d").strftime("%d/%m")
        for m in movements_by_date
    ]
    movement_date_counts = [m['count'] for m in movements_by_date]

    # Solo los últimos 8 días
    movement_dates = movement_dates[-8:]
    movement_date_counts = movement_date_counts[-8:]

    context = {
        'clients_count': Client.objects.count(),
        'accounts_count': Account.objects.count(),
        'judicial_holds_count': JudicialHold.objects.count(),
        'account_movements_count': AccountMovement.objects.count(),
        'movement_counts': movement_counts,
        'movement_labels': list(movement_types.values()),
        'movement_dates': movement_dates,
        'movement_date_counts': movement_date_counts,
    }
    return render(request, 'bankingsys/index.html', context)
