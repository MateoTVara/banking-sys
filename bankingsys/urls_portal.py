from django.urls import path
from .views import client_portal

app_name = 'portal'

urlpatterns = [
    path('', client_portal.portal_dashboard, name='dashboard'),
    path('deposito/', client_portal.portal_deposito, name='deposito'),
    path('retiro/', client_portal.portal_retiro, name='retiro'),
]
