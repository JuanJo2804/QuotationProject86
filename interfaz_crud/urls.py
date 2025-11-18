"""Rutas de la interfaz web (HTML) para `interfaz_crud`.

Contiene las rutas para las vistas basadas en plantillas (clientes y cotizaciones).
La API está definida en `urls_api.py` y se incluye desde `quotation_project/urls.py`.
"""

from django.urls import path
from . import views

app_name = 'interfaz_crud'

urlpatterns = [
    # URL de inicio del CRUD
    path('', views.inicio, name='inicio'),

    # URLs para Clientes
    path('clientes/', views.ListaClientes.as_view(), name='lista_clientes'),
    path('clientes/nuevo/', views.CrearCliente.as_view(), name='crear_cliente'),
    path('clientes/<int:pk>/', views.DetalleCliente.as_view(),
         name='detalle_cliente'),
    path('clientes/<int:pk>/editar/',
         views.EditarCliente.as_view(), name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/',
         views.EliminarCliente.as_view(), name='eliminar_cliente'),

    # URLs para Cotizaciones (CRUD)
    path('cotizaciones/', views.ListaCotizaciones.as_view(),
         name='lista_cotizaciones'),
    path('cotizaciones/nueva/', views.CrearCotizacion.as_view(),
         name='crear_cotizacion'),
    path('cotizaciones/<int:pk>/', views.DetalleCotizacion.as_view(),
         name='detalle_cotizacion'),
    path('cotizaciones/<int:pk>/editar/',
         views.EditarCotizacion.as_view(), name='editar_cotizacion'),
    path('cotizaciones/<int:pk>/eliminar/',
         views.EliminarCotizacion.as_view(), name='eliminar_cotizacion'),

    # Vista de cotización con cálculos (desde quotations)
    path('cotizaciones/calcular/', views.cotizacion_calcular,
         name='cotizacion_calcular'),
]
