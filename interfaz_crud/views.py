"""Vistas web (HTML) para la app `interfaz_crud`."""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm


def inicio(request):
    """Vista de inicio de la interfaz web.

    Renderiza `templates/inicio.html` (ahora extiende `base.html` del proyecto).
    Incluye estadísticas sobre clientes y cotizaciones.
    """
    from quotations.models import Quotation
    from django.utils import timezone
    from datetime import timedelta
    
    # Obtener estadísticas
    total_clientes = Cliente.objects.count()
    total_cotizaciones = Quotation.objects.count()
    
    # Cotizaciones del mes actual
    inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    cotizaciones_mes = Quotation.objects.filter(
        fecha_creacion__gte=inicio_mes
    ).count()
    
    context = {
        'total_clientes': total_clientes,
        'total_cotizaciones': total_cotizaciones,
        'cotizaciones_mes': cotizaciones_mes,
    }
    
    return render(request, 'interfaz_crud/inicio.html', context)


# Vistas para Clientes
class ListaClientes(ListView):
    model = Cliente
    template_name = 'interfaz_crud/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    ordering = ['-fecha_registro']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) | Q(correo__icontains=q)
            )
        return queryset


class CrearCliente(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'interfaz_crud/cliente_form.html'
    success_url = reverse_lazy('interfaz_crud:lista_clientes')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)


class EditarCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'interfaz_crud/cliente_form.html'
    success_url = reverse_lazy('interfaz_crud:lista_clientes')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado exitosamente.')
        return super().form_valid(form)


class EliminarCliente(DeleteView):
    model = Cliente
    template_name = 'interfaz_crud/cliente_confirm_delete.html'
    success_url = reverse_lazy('interfaz_crud:lista_clientes')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


class DetalleCliente(DetailView):
    model = Cliente
    template_name = 'interfaz_crud/cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener cotizaciones del modelo Quotation en la app quotations
        from quotations.models import Quotation
        context['cotizaciones'] = Quotation.objects.filter(cliente=self.object)
        return context



