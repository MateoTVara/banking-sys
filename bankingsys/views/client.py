from django.shortcuts import render
from ..models import Client
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import uuid
from django.views.decorators.http import require_POST

load_dotenv()

def client_list(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'bankingsys/client/clients.html', context)

def client_register(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'bankingsys/client/register.html', context)

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

@csrf_exempt
@require_POST
def register_client(request):
    client_type = request.POST.get("client_type")
    dni = request.POST.get("dni")
    ruc = request.POST.get("ruc")
    name = request.POST.get("name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    email = request.POST.get("email")

    if dni:
        if Client.objects.filter(dni=dni).exists():
            return JsonResponse({"error": "Ya existe un cliente con ese DNI"}, status=409)
    if ruc:
        if Client.objects.filter(ruc=ruc).exists():
            return JsonResponse({"error": "Ya existe un cliente con ese RUC"}, status=409)

    code = str(uuid.uuid4())[:8]

    if not name or not client_type:
        return JsonResponse({"error": "Datos incompletos"}, status=400)

    client = Client.objects.create(
        code=code,
        client_type=client_type,
        dni=dni,
        ruc=ruc,
        name=name,
        address=address,
        phone=phone,
        email=email
    )
    return JsonResponse({"success": True, "client_id": client.id, "code": code})