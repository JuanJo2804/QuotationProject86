"""
Formularios para la aplicación de cotizaciones
"""

from django import forms


class QuotationForm(forms.Form):
    """
    Formulario para recibir datos de cotización desde el frontend.
    """

    # Información del cliente
    nombre_cliente = forms.CharField(
        label='Nombre del Cliente',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ingrese el nombre del cliente'
        })
    )

    # Dimensiones de la marquilla
    ancho_cm = forms.FloatField(
        label='Ancho (cm)',
        min_value=0.1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 4'
        })
    )

    alto_cm = forms.FloatField(
        label='Alto (cm)',
        min_value=0.1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 3'
        })
    )

    espacio_entre_cm = forms.FloatField(
        label='Espacio entre marquillas (cm)',
        min_value=0,
        initial=0.5,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 0.5'
        })
    )

    # Cantidades
    cantidad_horizontal = forms.IntegerField(
        label='Marquillas horizontales',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 10'
        })
    )

    cantidad_vertical = forms.IntegerField(
        label='Marquillas verticales',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 10'
        })
    )

    cantidad = forms.IntegerField(
        label='Cantidad total a producir',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 1000'
        })
    )

    # Costos de producción
    valor_por_troquelada = forms.FloatField(
        label='Valor por troquelada',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 100'
        })
    )

    # Costos de material
    montaje = forms.FloatField(
        label='Valor del montaje',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 500'
        })
    )

    medida = forms.FloatField(
        label='Valor de la medida',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej: 200'
        })
    )

    # Costos de armado (opcionales)
    bolsa_individual = forms.FloatField(
        label='Bolsa individual',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    sellada = forms.FloatField(
        label='Sellada',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    cortada = forms.FloatField(
        label='Cortada',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    empaque_final = forms.FloatField(
        label='Empaque final',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    llenada_gel = forms.FloatField(
        label='Llenada gel',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    pin_soporte = forms.FloatField(
        label='Pin soporte',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    samblasted = forms.FloatField(
        label='Samblasted',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    # Otros materiales
    mo_rubber = forms.FloatField(
        label='MO Rubber',
        min_value=0,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    numero_plotter = forms.FloatField(
        label='Número Plotter',
        min_value=0,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    perforada = forms.FloatField(
        label='Perforada',
        min_value=0,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    guillotina = forms.FloatField(
        label='Guillotina',
        min_value=0,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '0'
        })
    )

    # Opcionales adicionales
    espesor = forms.ChoiceField(
        label='',
        choices=[
            ('2_mm', '2mm'),
            ('3_mm', '3mm'),
            ('1_mm', '1mm'),
            ('1.2_mm', '1.2mm'),
            ('1.5_mm', '1.5mm'),
            ('5_mm', '5mm'),
        ],
        initial='2_mm',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    def get_datos_cotizacion(self):
        """
        Convierte los datos del formulario al formato esperado por QuotationProcessor.

        Returns:
            dict: Datos formateados para calcular_cotizacion()
        """
        cleaned_data = self.cleaned_data

        return {
            'ancho_cm': float(cleaned_data['ancho_cm']),
            'alto_cm': float(cleaned_data['alto_cm']),
            'espacio_entre_cm': float(cleaned_data['espacio_entre_cm']),
            'cantidad_horizontal': int(cleaned_data['cantidad_horizontal']),
            'cantidad_vertical': int(cleaned_data['cantidad_vertical']),
            'cantidad': int(cleaned_data['cantidad']),
            'valor_por_troquelada': float(cleaned_data['valor_por_troquelada']),
            'montaje': float(cleaned_data.get('montaje') or 0),
            'medida': float(cleaned_data.get('medida') or 0),
            'espesor': cleaned_data.get('espesor', '2_mm'),
            'armado': {
                'bolsa_individual': float(cleaned_data.get('bolsa_individual') or 0),
                'sellada': float(cleaned_data.get('sellada') or 0),
                'cortada': float(cleaned_data.get('cortada') or 0),
                'empaque_final': float(cleaned_data.get('empaque_final') or 0),
                'llenada_gel': float(cleaned_data.get('llenada_gel') or 0),
                'pin_soporte': float(cleaned_data.get('pin_soporte') or 0),
                'samblasted': float(cleaned_data.get('samblasted') or 0),
            },
            'otros_materiales': {
                'mo_rubber': float(cleaned_data.get('mo_rubber') or 0),
                'numero_plotter': float(cleaned_data.get('numero_plotter') or 0),
                'perforada': float(cleaned_data.get('perforada') or 0),
                'guillotina': float(cleaned_data.get('guillotina') or 0),
            }
        }
