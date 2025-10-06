from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page.
    Exempts the login page and any URLs in the EXEMPT_URLS setting.
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
