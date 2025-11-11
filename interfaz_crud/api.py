"""interfaz_crud.api
---------------------
Aquí se definen los ViewSets de la API para clientes y cotizaciones.
Usamos los modelos que permanecen en la app `quotations` para no romper
las migraciones actuales. Los serializers están en `interfaz_crud.serializers`.

Endpoints expuestos (registrados en `urls_api.py`):
 - /api/clientes/      -> ClienteViewSet (lista, crear, actualizar, eliminar)
 - /api/cotizaciones/  -> CotizacionViewSet

Cada ViewSet usa SearchFilter para permitir búsquedas simples por nombre,
correo o descripción.
"""

from rest_framework import viewsets, filters
from .models import Cliente, Cotizacion
from .serializers import ClienteSerializer, CotizacionSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """API para gestionar clientes.

    Provee las operaciones CRUD sobre `quotations.models.Cliente` y utiliza
    `interfaz_crud.serializers.ClienteSerializer` para convertir datos a/desde JSON.
    """
    queryset = Cliente.objects.all().order_by('-fecha_registro')
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'correo']


class CotizacionViewSet(viewsets.ModelViewSet):
    """API para gestionar cotizaciones.

    Provee las operaciones CRUD sobre `quotations.models.Cotizacion`.
    """
    queryset = Cotizacion.objects.all().order_by('-fecha_creacion')
    serializer_class = CotizacionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cliente__nombre', 'descripcion']