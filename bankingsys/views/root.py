from django.shortcuts import redirect


def root_redirect(request):
    """
    Redirige a los usuarios según su grupo al hacer login o acceder a la raíz
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Redirigir según el grupo del usuario
    if request.user.groups.filter(name='clients').exists():
        return redirect('portal:dashboard')
    else:
        return redirect('bankingsys:index')
