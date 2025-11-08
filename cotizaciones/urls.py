from django.urls import path
from . import views

urlpatterns = [
    path('generar-pdf/', views.generar_cotizacion_pdf, name='generar_pdf'),
]
