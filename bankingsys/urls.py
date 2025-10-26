from django.urls import path
from . import views

app_name = 'bankingsys'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('', views.index, name='index'),
    path('exchange-rate/setup/', views.exchange_rate_setup, name='exchange_rate_setup'),
    
    path('tests/', views.test_list, name='tests'),
    path('users/', views.user_list, name='users'),
    path('clients/', views.client_list, name='clients'),
    path('clients/register/', views.client_register, name='client_register'),
    path('accounts/', views.account_list, name='accounts'),
    path('accounts/edit/', views.account_edit, name='account_edit'),
    path('accounts/register/', views.account_register, name='account_register'),
    path('judicial_holds/', views.judicial_hold_list, name='judicial_holds'),
    path('judicial_holds/register/', views.judicial_hold_register, name='judicial_hold_register'),
    path('judicial_holds/register_form/', views.judicial_hold_register_form, name='judicial_hold_register_form'),
    path('account_movements/', views.account_movement_list, name='account_movements'),

    path('api/fetch_identifier/', views.fetch_identifier_data, name='fetch_identifier'),
    path('api/register_client/', views.register_client, name='register_client'),
]