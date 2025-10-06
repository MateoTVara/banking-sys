from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('bankingsys:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.first_name} {user.last_name}!')
            next_url = request.GET.get('next', 'bankingsys:index')
            return redirect(next_url)
        else:
            messages.error(request, 'Nombre de usuario o contraseña inválidos.')

    return render(request, 'bankingsys/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('bankingsys:login')
