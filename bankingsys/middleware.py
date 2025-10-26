from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from datetime import date
from .models import ExchangeRate


class ExchangeRateRequiredMiddleware:
    """
    Middleware que requiere una tasa de cambio establecida para la fecha de hoy
    antes de permitir el acceso al sistema.
    Solo las páginas de inicio y cierre de sesión son accesibles sin la tasa de cambio.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # URLs exentas que deberian siempre estar disponibles
        exempt_urls = [
            '/admin/',
            '/static/',
            '/media/',
            reverse('bankingsys:login'),
            reverse('bankingsys:logout'),
            reverse('bankingsys:exchange_rate_setup'),
        ]
        
        # Verifica si la URL actual está en la lista de URLs exentas
        if any(path.startswith(url) for url in exempt_urls):
            response = self.get_response(request)
            return response

        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            response = self.get_response(request)
            return response

        # Verifica si existe la tasa de cambio de hoy
        today = date.today()
        exchange_rate_exists = ExchangeRate.objects.filter(date=today).exists()
        
        if not exchange_rate_exists:
            return redirect('bankingsys:exchange_rate_setup')
        
        response = self.get_response(request)
        return response


class LoginRequiredMiddleware:
    """
    Middleware que requiere que un usuario esté autenticado para ver cualquier página.
    Exime la página de inicio de sesión y cualquier URL en la configuración de EXEMPT_URLS.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que no requieren autenticación
        self.exempt_urls = [
            reverse('bankingsys:login'),
            '/admin/',
        ]
        if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
            self.exempt_urls += settings.LOGIN_EXEMPT_URLS

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            # Verifica si la URL actual está en la lista de URLs exentas
            if not any(path.startswith(url) for url in self.exempt_urls):
                login_url = reverse('bankingsys:login')
                return redirect(f'{login_url}?next={path}')
        
        response = self.get_response(request)
        return response

class ClientGroupRestrictionMiddleware:
    """
    Middleware que restringe el acceso a todas las vistas (excepto login y logout)
    para usuarios autenticados que pertenezcan al grupo 'clients'.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('bankingsys:login'),
            reverse('bankingsys:logout'),
            reverse('bankingsys:unauthorized'),  # Agrega la nueva vista
        ]

    def __call__(self, request):
        path = request.path_info
        # Solo aplica si el usuario está autenticado
        if request.user.is_authenticated:
            # Verifica si el usuario pertenece al grupo 'clients'
            if request.user.groups.filter(name='clients').exists():
                # Si la URL no es login ni logout, redirige a login
                if not any(path.startswith(url) for url in self.exempt_urls):
                    return redirect('bankingsys:unauthorized')
        return self.get_response(request)