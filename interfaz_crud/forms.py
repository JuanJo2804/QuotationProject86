from django import forms
from .models import Cliente

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