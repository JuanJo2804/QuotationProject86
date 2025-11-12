from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cotizacion/', views.cotizacion, name='cotizacion'),
]
