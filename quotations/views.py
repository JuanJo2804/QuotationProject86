from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def inicio(request):
    return HttpResponse("bienvenido a la pagina principal")


def cotizacion(request):
    return render(request, 'paginas/cotizacion.html')
