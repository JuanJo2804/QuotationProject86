"""Serializers para la API en `interfaz_crud`."""

from rest_framework import serializers
from .models import Cliente, Cotizacion


class ClienteSerializer(serializers.ModelSerializer):
    """Convierte instancias de `Cliente` a/desde JSON.

    Campos expuestos:
      - id
      - nombre
      - correo
      - fecha_registro (solo lectura)
    """

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'correo', 'fecha_registro']
        read_only_fields = ['fecha_registro']


class CotizacionSerializer(serializers.ModelSerializer):
    """Convierte instancias de `Cotizacion` a/desde JSON.

    Añade `nombre_cliente` (solo lectura) para facilitar respuestas legibles.
    """

    nombre_cliente = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Cotizacion
        fields = ['id', 'cliente', 'nombre_cliente', 'fecha_creacion', 'total', 'descripcion']
        read_only_fields = ['fecha_creacion']