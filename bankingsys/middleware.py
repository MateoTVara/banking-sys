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
            '/public/',  # Portal de clientes no requiere tipo de cambio
            '/login/',
            '/logout/',
            '/unauthorized/',  # Evitar loop de redirección
        ]
        
        # También exentar la ruta de configuración de tipo de cambio
        if path.startswith('/management/exchange-rate/setup/'):
            return self.get_response(request)
        
        # Verifica si la URL actual está en la lista de URLs exentas
        if any(path.startswith(url) for url in exempt_urls):
            response = self.get_response(request)
            return response

        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            response = self.get_response(request)
            return response

        # Los clientes no necesitan tipo de cambio (solo usan /public/)
        if request.user.groups.filter(name='clients').exists():
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

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            # URLs que no requieren autenticación
            exempt_urls = [
                '/login/',
                '/admin/',
            ]
            if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
                exempt_urls += settings.LOGIN_EXEMPT_URLS
            
            # Verifica si la URL actual está en la lista de URLs exentas
            if not any(path.startswith(url) for url in exempt_urls):
                return redirect(f'/login/?next={path}')
        
        response = self.get_response(request)
        return response

class ClientGroupRestrictionMiddleware:
    """
    Middleware que restringe el acceso de usuarios del grupo 'clients' solo al portal público.
    Los usuarios 'clients' solo pueden acceder a /public/, login y logout.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        # URLs exentas que siempre deben ser accesibles
        exempt_urls = [
            '/login/',
            '/logout/',
            '/unauthorized/',
            '/static/',
            '/media/',
            '/admin/',
            '/favicon.ico',
        ]
        
        # Solo aplica si el usuario está autenticado
        if request.user.is_authenticated:
            # Verifica si el usuario pertenece al grupo 'clients'
            if request.user.groups.filter(name='clients').exists():
                # Permitir acceso a /public/, raíz (/) y URLs exentas
                if path == '/' or path.startswith('/public/') or any(path.startswith(url) for url in exempt_urls):
                    return self.get_response(request)
                # Bloquear acceso a /management/ y otras rutas
                return redirect('/unauthorized/')
        return self.get_response(request)