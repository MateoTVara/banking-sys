from django.urls import path
from . import views

app_name = 'bankingsys'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('tests/', views.test_list, name='tests'),
    path('users/', views.user_list, name='users'),
    path('clients/', views.client_list, name='clients'),
    path('clients/register/', views.client_register, name='client_register'),
    path('accounts/', views.account_list, name='accounts'),
    path('judicial_holds/', views.judicial_hold_list, name='judicial_holds'),
    path('account_movements/', views.account_movement_list, name='account_movements'),
]