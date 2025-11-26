from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
import os
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from .forms.quotation_form import QuotationForm
from .business_logic.quotation_processor import QuotationProcessor
from .models import Quotation
from .utils.pdf_generator import generar_pdf_cotizacion

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
    
    # Filtro por período (fecha)
    periodo = request.GET.get('periodo', '')
    if periodo:
        hoy = timezone.now()
        if periodo == 'hoy':
            cotizaciones = cotizaciones.filter(fecha_creacion__date=hoy.date())
        elif periodo == 'semana':
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            cotizaciones = cotizaciones.filter(fecha_creacion__gte=inicio_semana)
        elif periodo == 'mes':
            inicio_mes = hoy.replace(day=1)
            cotizaciones = cotizaciones.filter(fecha_creacion__gte=inicio_mes)
        elif periodo == 'ano':
            inicio_ano = hoy.replace(month=1, day=1)
            cotizaciones = cotizaciones.filter(fecha_creacion__gte=inicio_ano)
    
    cotizaciones = cotizaciones.order_by('-fecha_creacion')
    
    context = {
        'cotizaciones': cotizaciones,
        'buscar': buscar,
        'periodo': periodo,
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

            # (La generación/descarga del PDF se realiza más abajo, luego de
            # intentar guardar la cotización si se solicitó.)

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

                        # Solo generar PDF y devolver descarga si NO es una petición AJAX
                        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
                            try:
                                datos['usuario'] = request.user
                                pdf_path = generar_pdf_cotizacion(dimensiones, resultado, gramos, datos, costos)
                                if os.path.exists(pdf_path):
                                    f = open(pdf_path, 'rb')
                                    return FileResponse(f, as_attachment=True, filename=os.path.basename(pdf_path))
                                else:
                                    messages.warning(request, '⚠️ PDF generado pero no se encontró el archivo para descargar.')
                            except Exception as e:
                                messages.warning(request, f'⚠️ No se pudo generar/descargar el PDF: {str(e)}')
                    else:
                        cotizacion = Quotation.objects.create(**datos_cotizacion)
                        messages.success(request, f'✅ Cotización guardada exitosamente para {datos["cliente"].nombre}')

                        # Solo generar PDF y devolver descarga si NO es una petición AJAX
                        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
                            try:
                                datos['usuario'] = request.user
                                pdf_path = generar_pdf_cotizacion(dimensiones, resultado, gramos, datos, costos)
                                if os.path.exists(pdf_path):
                                    f = open(pdf_path, 'rb')
                                    return FileResponse(f, as_attachment=True, filename=os.path.basename(pdf_path))
                                else:
                                    messages.warning(request, '⚠️ PDF generado pero no se encontró el archivo para descargar.')
                            except Exception as e:
                                messages.warning(request, f'⚠️ No se pudo generar/descargar el PDF: {str(e)}')
                    
                except Exception as e:
                    messages.error(request, f'❌ Error al guardar la cotización: {str(e)}')

            # Si se pidió JSON response (para AJAX)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)

            # NOTE: PDF generation and download will only run when the user
            # explicitly saves/creates the cotización (handled in the 'guardar'
            # branch above). For calculation-only requests (e.g. pressing
            # "Calcular"), we must NOT generate a PDF and should instead
            # render the template (or return JSON for AJAX). This prevents
            # interfering with the JSON response or the normal render flow.

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
