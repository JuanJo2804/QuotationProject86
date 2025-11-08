from django.shortcuts import render
from .pdf_generator import generar_pdf_cotizacion

def generar_cotizacion_pdf(request):
    datos = {
        "Dimensiones del molde": "18cm x 12cm",
        "Área total": "216 cm²",
        "Gramos totales": "46.08g",
        "Gramos por cm²": "0.21g",
        "Costo por gramo": "$29.00",
        "Material (por unidad)": "$33.41",
        "Total Material": "$33.41",
        "Total Armado": "$3.00",
        "Costo total": "$251.55",
        "Precio utilidad 45%": "$200000000",
        "Precio utilidad 28%": "$349.38",
        "Precio utilidad 17%": "$303.07",
        "Precio utilidad 11%": "$282.64",
    }
    return generar_pdf_cotizacion(datos)
