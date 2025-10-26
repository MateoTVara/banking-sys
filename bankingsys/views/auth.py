from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        # Redirigir según el grupo del usuario
        if request.user.groups.filter(name='clients').exists():
            return redirect('portal:dashboard')
        return redirect('bankingsys:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.first_name} {user.last_name}!')
            
            # Redirigir según el grupo del usuario
            if user.groups.filter(name='clients').exists():
                next_url = request.GET.get('next')
                if next_url and next_url.startswith('/public/'):
                    return redirect(next_url)
                return redirect('portal:dashboard')
            else:
                next_url = request.GET.get('next')
                if next_url and next_url.startswith('/management/'):
                    return redirect(next_url)
                return redirect('bankingsys:index')
        else:
            messages.error(request, 'Nombre de usuario o contraseña inválidos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


def unauthorized_view(request):
    """
    Vista para usuarios sin autorización (grupo 'clients').
    """
    return render(request, 'unauthorized.html')
