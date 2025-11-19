"""Rutas específicas de la API para la app `interfaz_crud`.

Se define un router de DRF que registra los ViewSets y expone las rutas
sin prefijo. El prefijo `/api/` se aplica desde `quotation_project/urls.py`.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register(r'clientes', api.ClienteViewSet)
router.register(r'cotizaciones', api.QuotationViewSet)

# NOTA: aquí usamos path('', include(...)) para evitar dobles prefijos
urlpatterns = [
    path('', include(router.urls)),
]