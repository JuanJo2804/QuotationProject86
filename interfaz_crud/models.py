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


class Cotizacion(models.Model):
    """
    Modelo para la tabla de cotizaciones. Asociado a `Cliente`.
    """
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='cotizaciones',
        help_text="Cliente al que pertenece esta cotización"
    )
    fecha_creacion = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True,
        help_text="Fecha y hora en que se creó la cotización"
    )
    total = models.DecimalField(
        "Total en pesos",
        max_digits=12,
        decimal_places=2,
        help_text="Monto total de la cotización"
    )
    descripcion = models.TextField(
        "Descripción",
        null=True,
        blank=True,
        help_text="Detalles adicionales de la cotización"
    )

    class Meta:
        app_label = 'interfaz_crud'
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Cotización #{self.id} - Cliente: {self.cliente.nombre}"