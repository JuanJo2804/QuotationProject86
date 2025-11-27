"""Utilities to generate a PDF for a quotation.

Provides the function `generar_pdf_cotizacion(dimensiones, resultado, gramos, datos, costos)`
which creates a nicely formatted PDF using reportlab.

Notes:
- Saves files to <BASE_DIR>/cotizaciones_pdf (created if missing).
- Uses `reportlab`. If not installed, ImportError will be raised.
"""
from datetime import datetime
import os
from decimal import Decimal

from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors


def _format_number(v):
    """Format numbers: ints without decimals, floats with 2 decimals."""
    try:
        if isinstance(v, Decimal):
            v = float(v)
        if isinstance(v, int):
            return f"{v:,}"
        return f"{v:,.2f}"
    except Exception:
        return str(v)


def _format_money(v):
    """Format a numeric value as currency with dollar sign."""
    try:
        if isinstance(v, Decimal):
            v = float(v)
        return f"${v:,.2f}"
    except Exception:
        return str(v)


def generar_pdf_cotizacion(dimensiones, resultado, gramos, datos, costos):
    """Genera un PDF con los datos de la cotización.

    Parámetros:
    - dimensiones: dict con claves como 'largo_total', 'alto_total', 'area_total'
    - resultado: dict con resultados generales (incluye 'costo_por_gramo', 'valor_material', etc.)
    - gramos: dict con 'gramos_total', 'gramos_por_cm2'
    - datos: dict con datos de entrada (incluye 'montaje', 'medida', 'armado'...)
    - costos: dict con desgloses de costos de producción

    El archivo se guarda como `cotizacion_<YYYYMMDD_HHMMSS>.pdf` en la carpeta
    `<BASE_DIR>/cotizaciones_pdf`.
    """
    # Local de salida
    base_dir = getattr(settings, 'BASE_DIR', os.getcwd())
    out_dir = os.path.join(base_dir, 'cotizaciones_pdf')
    os.makedirs(out_dir, exist_ok=True)

    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(out_dir, f'cotizacion_{fecha}.pdf')

    # Document setup
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    story = []

    # Header: include client and user (if provided in `datos`)
    cliente = None
    usuario = None
    if isinstance(datos, dict):
        cliente = datos.get('cliente')
        usuario = datos.get('usuario')

    title_style = ParagraphStyle('title', parent=styles['Heading1'], alignment=1, fontSize=18)
    story.append(Paragraph('COTIZACIÓN DETALLADA', title_style))
    story.append(Spacer(1, 6))

    # Client / user info
    info_lines = []
    if cliente is not None:
        try:
            # `cliente` may be a model instance with attributes `nombre`, `correo`, `telefono`
            nombre = getattr(cliente, 'nombre', str(cliente))
            correo = getattr(cliente, 'correo', '')
            telefono = getattr(cliente, 'telefono', '')
            info_lines.append(f"Cliente: {nombre}")
            if correo:
                info_lines.append(f"Correo: {correo}")
            if telefono:
                info_lines.append(f"Teléfono: {telefono}")
        except Exception:
            info_lines.append(f"Cliente: {str(cliente)}")

    if usuario is not None:
        try:
            usuario_nombre = getattr(usuario, 'get_full_name', None)
            if callable(usuario_nombre):
                usuario_nombre = usuario.get_full_name() or getattr(usuario, 'username', str(usuario))
            else:
                usuario_nombre = getattr(usuario, 'username', str(usuario))
            info_lines.append(f"Realizado por: {usuario_nombre}")
        except Exception:
            info_lines.append(f"Realizado por: {str(usuario)}")

    if info_lines:
        for line in info_lines:
            story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 6))

    # Spacer already added below for consistency
    # (the spacer for title was added above)

    # Dimensiones y resumen
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Heading2'], fontSize=12)
    story.append(Paragraph('Dimensiones y Resumen', subtitle_style))
    story.append(Spacer(1, 4))

    dims_table_data = [
        ['Dimensiones del molde:', f"{dimensiones.get('largo_total', '')}cm x {dimensiones.get('alto_total', '')}cm"],
        ['Área total:', f"{_format_number(dimensiones.get('area_total', ''))} cm²"],
        ['Gramos totales:', f"{_format_number(gramos.get('gramos_total', ''))} g"],
        ['Gramos por cm²:', f"{_format_number(gramos.get('gramos_por_cm2', ''))} g"],
        ['Costo por gramo:', _format_money(resultado.get('costo_por_gramo', 0))],
    ]
    t = Table(dims_table_data, colWidths=[90*mm, 70*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # Costos de material
    story.append(Paragraph('COSTOS DE MATERIAL', subtitle_style))
    story.append(Spacer(1, 4))
    material_table = [
        ['Material (por unidad):', _format_money(resultado.get('valor_material', 0))],
        ['Montaje:', _format_money(datos.get('montaje', 0))],
        ['Medida:', _format_money(datos.get('medida', 0))],
        ['Total Material:', _format_money(resultado.get('total_material', 0))],
    ]
    t2 = Table(material_table, colWidths=[90*mm, 70*mm])
    t2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    # Costos de armado
    story.append(Paragraph('COSTOS DE ARMADO', subtitle_style))
    story.append(Spacer(1, 4))
    armado = datos.get('armado', {}) if isinstance(datos, dict) else {}
    armado_table = []
    for concepto, valor in armado.items():
        armado_table.append([str(concepto), _format_money(valor)])
    armado_table.append(['Total Armado:', _format_money(resultado.get('total_armado', 0))])
    t3 = Table(armado_table, colWidths=[90*mm, 70*mm])
    t3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
    ]))
    story.append(t3)
    story.append(Spacer(1, 8))

    # Costos de producción (desglose)
    story.append(Paragraph('COSTOS DE PRODUCCIÓN', subtitle_style))
    story.append(Spacer(1, 4))
    prod_table = []
    for k, v in (costos or {}).items():
        # Mostrar como dinero si la clave contiene 'costo' o 'precio'
        key_lower = str(k).lower()
        is_numeric = isinstance(v, (int, float, Decimal))
        if is_numeric:
            if 'costo' in key_lower or 'precio' in key_lower or 'valor' in key_lower or 'total' in key_lower:
                prod_table.append([str(k), _format_money(v)])
            else:
                prod_table.append([str(k), _format_number(v)])
        else:
            prod_table.append([str(k), str(v)])

    if not prod_table:
        prod_table.append(['--', 'No hay costos de producción disponibles'])

    t4 = Table(prod_table, colWidths=[90*mm, 70*mm])
    t4.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
    ]))
    story.append(t4)
    story.append(Spacer(1, 12))

    # Footer with generated timestamp
    footer = Paragraph(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(footer)

    # Build PDF
    doc.build(story)

    return filename
