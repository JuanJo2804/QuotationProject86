from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cotizar/', views.cotizacion, name='cotizar'),
    path('cotizaciones/', views.lista_cotizaciones, name='lista_cotizaciones'),
    path('editar/<int:cotizacion_id>/', views.cotizacion, name='editar_cotizacion'),
    path('eliminar/<int:cotizacion_id>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
]
