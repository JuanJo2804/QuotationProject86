from django.db import models
from interfaz_crud.models import Cliente


class Quotation(models.Model):
    """
    Cotización completa con todos los datos de entrada y resultados calculados.
    """
    # ========== RELACIÓN CON CLIENTE ==========
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='cotizaciones',
        help_text="Cliente que solicita la cotización"
    )
    
    # ========== DIMENSIONES DE LA MARQUILLA ==========
    ancho_cm = models.FloatField(
        "Ancho (cm)",
        help_text="Ancho de la marquilla en centímetros"
    )
    
    alto_cm = models.FloatField(
        "Alto (cm)",
        help_text="Alto de la marquilla en centímetros"
    )
    
    espacio_entre_cm = models.FloatField(
        "Espacio entre marquillas (cm)",
        default=0.5,
        help_text="Espacio entre marquillas en el molde"
    )
    
    # ========== CANTIDADES ==========
    cantidad_horizontal = models.IntegerField(
        "Marquillas horizontales",
        help_text="Cantidad de marquillas en horizontal por molde"
    )
    
    cantidad_vertical = models.IntegerField(
        "Marquillas verticales",
        help_text="Cantidad de marquillas en vertical por molde"
    )
    
    cantidad = models.IntegerField(
        "Cantidad total a producir",
        help_text="Cantidad total de marquillas a producir"
    )
    
    # ========== COSTOS DE PRODUCCIÓN ==========
    valor_por_troquelada = models.FloatField(
        "Valor por troquelada",
        help_text="Costo de la troquelada"
    )
    
    montaje = models.FloatField(
        "Valor del montaje",
        default=0,
        help_text="Costo del montaje"
    )
    
    medida = models.FloatField(
        "Valor de la medida",
        default=0,
        help_text="Costo de la medida"
    )
    
    # ========== TIPO DE MATERIAL ==========
    ESPESOR_CHOICES = [
        ('2_mm', '2mm'),
        ('3_mm', '3mm'),
        ('1_mm', '1mm'),
        ('1.2_mm', '1.2mm'),
        ('1.5_mm', '1.5mm'),
        ('5_mm', '5mm'),
    ]
    
    espesor = models.CharField(
        "Espesor",
        max_length=10,
        choices=ESPESOR_CHOICES,
        default='2_mm',
        help_text="Espesor del material"
    )
    
    # ========== COSTOS DE ARMADO ==========
    bolsa_individual = models.FloatField(
        "Bolsa individual",
        default=0,
        help_text="Costo de bolsa individual"
    )
    
    sellada = models.FloatField(
        "Sellada",
        default=0,
        help_text="Costo de sellado"
    )
    
    cortada = models.FloatField(
        "Cortada",
        default=0,
        help_text="Costo de corte"
    )
    
    empaque_final = models.FloatField(
        "Empaque final",
        default=0,
        help_text="Costo de empaque final"
    )
    
    llenada_gel = models.FloatField(
        "Llenada gel",
        default=0,
        help_text="Costo de llenado de gel"
    )
    
    pin_soporte = models.FloatField(
        "Pin soporte",
        default=0,
        help_text="Costo de pin soporte"
    )
    
    samblasted = models.FloatField(
        "Samblasted",
        default=0,
        help_text="Costo de proceso samblasted"
    )
    
    # ========== OTROS MATERIALES ==========
    mo_rubber = models.FloatField(
        "MO Rubber",
        default=0,
        help_text="Costo de mano de obra en rubber"
    )
    
    numero_plotter = models.FloatField(
        "Número Plotter",
        default=0,
        help_text="Costo de número plotter"
    )
    
    perforada = models.FloatField(
        "Perforada",
        default=0,
        help_text="Costo de perforado"
    )
    
    guillotina = models.FloatField(
        "Guillotina",
        default=0,
        help_text="Costo de guillotina"
    )
    
    # ========== DIMENSIONES CALCULADAS ==========
    largo_total_cm = models.FloatField(
        "Largo total del molde (cm)",
        null=True,
        blank=True,
        help_text="Largo total del molde incluyendo márgenes"
    )
    
    alto_total_cm = models.FloatField(
        "Alto total del molde (cm)",
        null=True,
        blank=True,
        help_text="Alto total del molde incluyendo márgenes"
    )
    
    area_total_cm2 = models.FloatField(
        "Área total (cm²)",
        null=True,
        blank=True,
        help_text="Área total del molde en centímetros cuadrados"
    )
    
    # ========== GRAMOS ==========
    gramos_total = models.FloatField(
        "Gramos totales",
        null=True,
        blank=True,
        help_text="Gramos totales de material del molde"
    )
    
    gramos_por_cm2 = models.FloatField(
        "Gramos por cm²",
        null=True,
        blank=True,
        help_text="Gramos de material por centímetro cuadrado"
    )
    
    costo_por_gramo = models.FloatField(
        "Costo por gramo",
        null=True,
        blank=True,
        help_text="Costo unitario por gramo de material"
    )
    
    # ========== COSTOS CALCULADOS ==========
    material = models.FloatField(
        "Costo de material (por unidad)",
        null=True,
        blank=True,
        help_text="Costo de material por marquilla"
    )
    
    total_material = models.FloatField(
        "Total material",
        null=True,
        blank=True,
        help_text="Total de material (material + montaje + medida)"
    )
    
    total_armado = models.FloatField(
        "Total armado",
        null=True,
        blank=True,
        help_text="Total de costos de armado/empaquetado"
    )
    
    otros_materiales_total = models.FloatField(
        "Total otros materiales",
        null=True,
        blank=True,
        help_text="Total de otros materiales y procesos"
    )
    
    # ========== CIF (Costos Indirectos de Fabricación) ==========
    cif_8 = models.FloatField(
        "CIF 8%",
        null=True,
        blank=True,
        help_text="CIF calculado al 8%"
    )
    
    cif_10 = models.FloatField(
        "CIF 10%",
        null=True,
        blank=True,
        help_text="CIF calculado al 10%"
    )
    
    cif_15 = models.FloatField(
        "CIF 15%",
        null=True,
        blank=True,
        help_text="CIF calculado al 15%"
    )
    
    # ========== ADMINISTRACIÓN ==========
    admon = models.FloatField(
        "Administración",
        null=True,
        blank=True,
        help_text="Costos de administración"
    )
    
    # ========== COSTO TOTAL ==========
    costo_total = models.FloatField(
        "Costo total de producción",
        null=True,
        blank=True,
        help_text="Costo total de producir la marquilla"
    )
    
    # ========== PRECIOS DE VENTA ==========
    precio_utilidad_45 = models.FloatField(
        "Precio con utilidad 45%",
        null=True,
        blank=True,
        help_text="Precio de venta con 45% de utilidad"
    )
    
    precio_utilidad_28 = models.FloatField(
        "Precio con utilidad 28%",
        null=True,
        blank=True,
        help_text="Precio de venta con 28% de utilidad"
    )
    
    precio_utilidad_17 = models.FloatField(
        "Precio con utilidad 17%",
        null=True,
        blank=True,
        help_text="Precio de venta con 17% de utilidad"
    )
    
    precio_utilidad_11 = models.FloatField(
        "Precio con utilidad 11%",
        null=True,
        blank=True,
        help_text="Precio de venta con 11% de utilidad"
    )
    
    # ========== METADATOS ==========
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('aprobada', 'Aprobada'),
    ]
    
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        help_text="Estado de la cotización"
    )
    
    fecha_creacion = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True,
        help_text="Fecha y hora en que se creó la cotización"
    )
    
    fecha_modificacion = models.DateTimeField(
        "Fecha de modificación",
        auto_now=True,
        help_text="Fecha y hora de la última modificación"
    )
    
    class Meta:
        app_label = 'quotations'
        db_table = 'quotation'
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente.nombre} ({self.cantidad} unidades)"
    
    @property
    def nombre_cliente(self):
        """Retorna el nombre del cliente desde la relación."""
        return self.cliente.nombre if self.cliente else ""
    
    @property
    def marquillas_por_molde(self):
        """Calcula cuántas marquillas salen por molde."""
        return self.cantidad_horizontal * self.cantidad_vertical
    
    @property
    def precio_recomendado(self):
        """Retorna el precio con utilidad media (28%)."""
        return self.precio_utilidad_28 if self.precio_utilidad_28 else 0
