from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generar_pdf_cotizacion(datos):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cotizacion.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "COTIZACIÓN ")
    y -= 40

    p.setFont("Helvetica", 12)
    for key, value in datos.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 100:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    return response
