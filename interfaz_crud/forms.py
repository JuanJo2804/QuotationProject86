from django import forms
from .models import Cliente, Cotizacion

class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes."""
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}) ,
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección (calle, número, ciudad)'}),
        }

class CotizacionForm(forms.ModelForm):
    """Formulario para crear y editar cotizaciones."""
    class Meta:
        model = Cotizacion
        fields = ['cliente', 'total', 'descripcion']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }