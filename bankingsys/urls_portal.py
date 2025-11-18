from django.urls import path
from .views import client_portal

app_name = 'portal'

urlpatterns = [
    path('', client_portal.mis_cuentas, name='dashboard'),
    path('deposito/', client_portal.portal_deposito, name='deposito'),
    path('retiro/', client_portal.portal_retiro, name='retiro'),
    path('transferencia/', client_portal.portal_transferencia, name='transferencia'),
    path('cuentas-plazo/', client_portal.portal_cuentas_plazo, name='cuentas_plazo'),
    path('cancelar-plazo/<int:account_id>/', client_portal.cancelar_cuenta_plazo, name='cancelar_plazo'),
    path('renovar-plazo/<int:account_id>/', client_portal.renovar_cuenta_plazo, name='renovar_plazo'),
    # Gestión de cuentas
    path('apertura-cuenta/', client_portal.apertura_cuenta, name='apertura_cuenta'),
    path('cierre-cuenta/', client_portal.cierre_cuenta, name='cierre_cuenta'),
    path('mis-cuentas/', client_portal.mis_cuentas, name='mis_cuentas'),
    path('mis-movimientos/', client_portal.mis_movimientos, name='mis_movimientos'),
]