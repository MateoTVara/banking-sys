from django.shortcuts import render
from ..models import JudicialHold


def judicial_hold_list(request):
    judicial_holds = JudicialHold.objects.all()
    context = {
        'judicial_holds': judicial_holds
    }
    return render(request, 'bankingsys/judicial_hold/judicial_holds.html', context)
