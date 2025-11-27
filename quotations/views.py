from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from .forms.quotation_form import QuotationForm
from .business_logic.quotation_processor import QuotationProcessor
from .models import Quotation
from Filterss.quotation_filter_form import QuotationFilterForm # Importamos desde la nueva ubicación

# Create your views here.


def inicio(request):
    """Vista de inicio/home con plantilla HTML"""
    return render(request, 'interfaz_crud/inicio.html')


def lista_cotizaciones(request):
    """Vista de lista de cotizaciones con filtros"""
    cotizaciones = Quotation.objects.select_related('cliente').all()
    
    # Filtro por búsqueda de cliente
    buscar = request.GET.get('buscar', '')
    if buscar:
        cotizaciones = cotizaciones.filter(
            Q(cliente__nombre__icontains=buscar) |
            Q(cliente__correo__icontains=buscar)
        )
    
    # Filtro por estado
    estado = request.GET.get('estado', '')
    if estado:
        cotizaciones = cotizaciones.filter(estado=estado)
    
    # Filtro por fecha de creación
    fecha_creacion = request.GET.get('fecha_creacion', '')
    if fecha_creacion:
        cotizaciones = cotizaciones.filter(fecha_creacion__date=fecha_creacion)
    
    cotizaciones = cotizaciones.order_by('-fecha_creacion')
    
    context = {
        'cotizaciones': cotizaciones,
        'buscar': buscar,
        'estado': estado,
        'fecha_creacion': fecha_creacion,
    }
    return render(request, 'paginas/lista_cotizaciones.html', context)


def cotizacion(request, cotizacion_id=None):
    """
    Vista principal de cotización con diseño mejorado.
    Maneja el formulario, procesa los cálculos y opcionalmente guarda en BD.
    Si recibe cotizacion_id, edita la cotización existente.
    """
    resultado = None
    cotizacion_existente = None
    
    # Si hay ID, estamos editando
    if cotizacion_id:
        cotizacion_existente = get_object_or_404(Quotation, id=cotizacion_id)
        form = QuotationForm(initial={
            'cliente': cotizacion_existente.cliente,
            'ancho_cm': cotizacion_existente.ancho_cm,
            'alto_cm': cotizacion_existente.alto_cm,
            'espacio_entre_cm': cotizacion_existente.espacio_entre_cm,
            'cantidad_horizontal': cotizacion_existente.cantidad_horizontal,
            'cantidad_vertical': cotizacion_existente.cantidad_vertical,
            'cantidad': cotizacion_existente.cantidad,
            'valor_por_troquelada': cotizacion_existente.valor_por_troquelada,
            'montaje': cotizacion_existente.montaje,
            'medida': cotizacion_existente.medida,
            'espesor': cotizacion_existente.espesor,
            'bolsa_individual': cotizacion_existente.bolsa_individual,
            'sellada': cotizacion_existente.sellada,
            'cortada': cotizacion_existente.cortada,
            'empaque_final': cotizacion_existente.empaque_final,
            'llenada_gel': cotizacion_existente.llenada_gel,
            'pin_soporte': cotizacion_existente.pin_soporte,
            'samblasted': cotizacion_existente.samblasted,
            'mo_rubber': cotizacion_existente.mo_rubber,
            'numero_plotter': cotizacion_existente.numero_plotter,
            'perforada': cotizacion_existente.perforada,
            'guillotina': cotizacion_existente.guillotina,
        })
    else:
        form = QuotationForm()

    if request.method == 'POST':
        form = QuotationForm(request.POST)

        if form.is_valid():
            # Obtener datos del formulario
            datos = form.get_datos_cotizacion()

            # Procesar cotización
            processor = QuotationProcessor()
            resultado = processor.calcular_cotizacion(datos)

            # Verificar si se presionó el botón "Guardar"
            if 'guardar' in request.POST and resultado.get('success'):
                try:
                    # Extraer resultados calculados
                    dimensiones = resultado['dimensiones']
                    gramos = resultado['gramos']
                    costos = resultado['costos']
                    armado_data = datos.get('armado', {})
                    otros_data = datos.get('otros_materiales', {})

                    # Datos comunes para crear o actualizar
                    datos_cotizacion = {
                        'cliente': datos['cliente'],
                        'ancho_cm': datos['ancho_cm'],
                        'alto_cm': datos['alto_cm'],
                        'espacio_entre_cm': datos['espacio_entre_cm'],
                        'cantidad_horizontal': datos['cantidad_horizontal'],
                        'cantidad_vertical': datos['cantidad_vertical'],
                        'cantidad': datos['cantidad'],
                        'valor_por_troquelada': datos['valor_por_troquelada'],
                        'montaje': datos['montaje'],
                        'medida': datos['medida'],
                        'espesor': datos.get('espesor', '2_mm'),
                        'bolsa_individual': armado_data.get('bolsa_individual', 0),
                        'sellada': armado_data.get('sellada', 0),
                        'cortada': armado_data.get('cortada', 0),
                        'empaque_final': armado_data.get('empaque_final', 0),
                        'llenada_gel': armado_data.get('llenada_gel', 0),
                        'pin_soporte': armado_data.get('pin_soporte', 0),
                        'samblasted': armado_data.get('samblasted', 0),
                        'mo_rubber': otros_data.get('mo_rubber', 0),
                        'numero_plotter': otros_data.get('numero_plotter', 0),
                        'perforada': otros_data.get('perforada', 0),
                        'guillotina': otros_data.get('guillotina', 0),
                        'largo_total_cm': dimensiones['largo_total'],
                        'alto_total_cm': dimensiones['alto_total'],
                        'area_total_cm2': dimensiones['area_total'],
                        'gramos_total': gramos['gramos_total'],
                        'gramos_por_cm2': gramos['gramos_por_cm2'],
                        'costo_por_gramo': resultado['costo_por_gramo'],
                        'material': costos['material'],
                        'total_material': costos['total_material'],
                        'total_armado': costos['total_armado'],
                        'otros_materiales_total': costos['otros_materiales_total'],
                        'cif_8': costos['cif_8'],
                        'cif_10': costos['cif_10'],
                        'cif_15': costos['cif_15'],
                        'admon': costos['admon'],
                        'costo_total': costos['costo_total'],
                        'precio_utilidad_45': costos['precio_utilidad_45'],
                        'precio_utilidad_28': costos['precio_utilidad_28'],
                        'precio_utilidad_17': costos['precio_utilidad_17'],
                        'precio_utilidad_11': costos['precio_utilidad_11']
                    }

                    # Actualizar o crear cotización
                    if cotizacion_existente:
                        for key, value in datos_cotizacion.items():
                            setattr(cotizacion_existente, key, value)
                        cotizacion_existente.save()
                        messages.success(request, f'✅ Cotización actualizada exitosamente para {datos["cliente"].nombre}')
                        return redirect('quotations:lista_cotizaciones')
                    else:
                        cotizacion = Quotation.objects.create(**datos_cotizacion)
                        messages.success(request, f'✅ Cotización guardada exitosamente para {datos["cliente"].nombre}')
                    
                except Exception as e:
                    messages.error(request, f'❌ Error al guardar la cotización: {str(e)}')

            # Si se pidió JSON response (para AJAX)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)

    context = {
        'form': form,
        'resultado': resultado,
        'editando': cotizacion_existente is not None
    }

    return render(request, 'paginas/cotizaciones.html', context)


def eliminar_cotizacion(request, cotizacion_id):
    """Vista para eliminar una cotización"""
    cotizacion = get_object_or_404(Quotation, id=cotizacion_id)
    
    if request.method == 'POST':
        cliente_nombre = cotizacion.cliente.nombre
        cotizacion.delete()
        messages.success(request, f'✅ Cotización eliminada exitosamente para {cliente_nombre}')
        return redirect('quotations:lista_cotizaciones')
    
    context = {
        'cotizacion': cotizacion
    }
    return render(request, 'paginas/eliminar_cotizacion.html', context)


def cambiar_estado(request, cotizacion_id):
    """Vista para cambiar el estado de una cotización entre Pendiente, Enviada y Aprobada"""
    cotizacion = get_object_or_404(Quotation, id=cotizacion_id)
    
    if request.method == 'POST':
        # Cambiar el estado en ciclo: pendiente -> enviada -> aprobada -> pendiente
        if cotizacion.estado == 'pendiente':
            cotizacion.estado = 'enviada'
            messages.success(request, f'✅ Cotización marcada como Enviada para {cotizacion.cliente.nombre}')
        elif cotizacion.estado == 'enviada':
            cotizacion.estado = 'aprobada'
            messages.success(request, f'✅ Cotización marcada como Aprobada para {cotizacion.cliente.nombre}')
        else:
            cotizacion.estado = 'pendiente'
            messages.success(request, f'✅ Cotización marcada como Pendiente para {cotizacion.cliente.nombre}')
        
        cotizacion.save()
    
    return redirect('quotations:lista_cotizaciones')
