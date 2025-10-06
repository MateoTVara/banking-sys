from django.shortcuts import render
from ..models import Client
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

def client_list(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'bankingsys/client/clients.html', context)

def client_register(request):
    return render(request, 'bankingsys/client/register.html')

@csrf_exempt
def fetch_identifier_data(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        api_key = os.getenv("API_KEY")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        if identifier and len(identifier) == 8:
            # DNI
            url = f"https://api.decolecta.com/v1/reniec/dni?numero={identifier}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return JsonResponse({
                    "type": "dni",
                    "full_name": data.get("full_name", "")
                })
            return JsonResponse({"error": "No encontrado"}, status=404)
        elif identifier and len(identifier) == 11:
            # RUC
            url = f"https://api.decolecta.com/v1/sunat/ruc/full?numero={identifier}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return JsonResponse({
                    "type": "ruc",
                    "razon_social": data.get("razon_social", ""),
                    "direccion": data.get("direccion", "")
                })
            return JsonResponse({"error": "No encontrado"}, status=404)
        else:
            return JsonResponse({"error": "Identificador inválido"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)