from django.urls import path
from .views import client_portal

app_name = 'portal'

urlpatterns = [
    path('', client_portal.portal_dashboard, name='dashboard'),
]
