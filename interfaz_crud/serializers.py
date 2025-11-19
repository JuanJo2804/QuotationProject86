"""Serializers para la API en `interfaz_crud`."""

from rest_framework import serializers
from .models import Cliente
from quotations.models import Quotation


class ClienteSerializer(serializers.ModelSerializer):
    """Convierte instancias de `Cliente` a/desde JSON.

    Campos expuestos:
      - id
      - nombre
      - correo
      - telefono
      - direccion
      - fecha_registro (solo lectura)
    """

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'correo', 'telefono', 'direccion', 'fecha_registro']
        read_only_fields = ['fecha_registro']


class QuotationSerializer(serializers.ModelSerializer):
    """Convierte instancias de `Quotation` a/desde JSON.

    Añade `nombre_cliente` (solo lectura) para facilitar respuestas legibles.
    """

    nombre_cliente = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Quotation
        fields = [
            'id', 'cliente', 'nombre_cliente', 'fecha_creacion', 'fecha_modificacion',
            'ancho_cm', 'alto_cm', 'cantidad', 'costo_total', 'precio_utilidad_28'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']