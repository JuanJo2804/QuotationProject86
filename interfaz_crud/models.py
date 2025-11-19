from django.db import models


class Cliente(models.Model):
    """
    Modelo para la tabla de clientes.
    """
    nombre = models.CharField(
        max_length=255,
        help_text="Nombre completo del cliente"
    )
    correo = models.EmailField(
        unique=True,
        help_text="Correo electrónico del cliente (debe ser único)"
    )
    telefono = models.CharField(
        "Teléfono",
        max_length=20,
        null=True,
        blank=True,
        help_text="Número telefónico del cliente (opcional)"
    )
    direccion = models.CharField(
        "Dirección",
        max_length=255,
        null=True,
        blank=True,
        help_text="Dirección física del cliente (opcional)"
    )
    fecha_registro = models.DateTimeField(
        "Fecha de registro",
        auto_now_add=True,
        help_text="Fecha y hora en que se registró el cliente"
    )

    class Meta:
        app_label = 'interfaz_crud'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre} ({self.correo})"