"""interfaz_crud.api
---------------------
Aquí se definen los ViewSets de la API para clientes y cotizaciones.

Endpoints expuestos (registrados en `urls_api.py`):
 - /api/clientes/      -> ClienteViewSet (lista, crear, actualizar, eliminar)
 - /api/cotizaciones/  -> QuotationViewSet (usa el modelo Quotation de quotations app)

Cada ViewSet usa SearchFilter para permitir búsquedas simples por nombre,
correo o descripción.
"""

from rest_framework import viewsets, filters
from .models import Cliente
from quotations.models import Quotation
from .serializers import ClienteSerializer, QuotationSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """API para gestionar clientes.

    Provee las operaciones CRUD sobre `interfaz_crud.models.Cliente` y utiliza
    `interfaz_crud.serializers.ClienteSerializer` para convertir datos a/desde JSON.
    """
    queryset = Cliente.objects.all().order_by('-fecha_registro')
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'correo']


class QuotationViewSet(viewsets.ModelViewSet):
    """API para gestionar cotizaciones.

    Provee las operaciones CRUD sobre `quotations.models.Quotation`.
    """
    queryset = Quotation.objects.all().order_by('-fecha_creacion')
    serializer_class = QuotationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cliente__nombre']