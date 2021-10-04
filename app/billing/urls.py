from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('account/', views.account_create, name='account_create'),
    path('account/<int:id>/', views.account_get, name='account_get'),
]