from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms.quotation_form import QuotationForm
from .business_logic.quotation_processor import QuotationProcessor

# Create your views here.


def inicio(request):
    """Vista de inicio/home con plantilla HTML"""
    return render(request, 'interfaz_crud/inicio.html')


def cotizacion(request):
    """
    Vista principal de cotización con diseño mejorado.
    Maneja el formulario y procesa los cálculos.
    """
    resultado = None
    form = QuotationForm()

    if request.method == 'POST':
        form = QuotationForm(request.POST)

        if form.is_valid():
            # Obtener datos del formulario
            datos = form.get_datos_cotizacion()

            # Procesar cotización
            processor = QuotationProcessor()
            resultado = processor.calcular_cotizacion(datos)

            # Si se pidió JSON response (para AJAX)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)

    context = {
        'form': form,
        'resultado': resultado
    }

    return render(request, 'paginas/cotizaciones.html', context)
