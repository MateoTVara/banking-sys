from django.urls import path
from .views import client_portal

app_name = 'portal'

urlpatterns = [
    path('', client_portal.portal_dashboard, name='dashboard'),
    path('deposito/', client_portal.portal_deposito, name='deposito'),
    path('retiro/', client_portal.portal_retiro, name='retiro'),
    path('transferencia/', client_portal.portal_transferencia, name='transferencia'),
    path('cuentas-plazo/', client_portal.portal_cuentas_plazo, name='cuentas_plazo'),
    path('cancelar-plazo/<int:account_id>/', client_portal.cancelar_cuenta_plazo, name='cancelar_plazo'),
    path('renovar-plazo/<int:account_id>/', client_portal.renovar_cuenta_plazo, name='renovar_plazo'),
]