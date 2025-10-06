from django.shortcuts import render
from ..models import Test


def test_list(request):
    tests = Test.objects.all()
    context = {
        'tests': tests
    }
    return render(request, 'bankingsys/test/tests.html', context)
