"""
Sistema de Cotización para Marquillas en PVC

Este módulo implementa el proceso completo de cotización:
1. Calcula área del molde según dimensiones y disposición
2. Determina gramos totales según tabla de referencia
3. Calcula costos de producción basados en área y gramos
4. Genera cotización final con diferentes porcentajes

Adaptado para funcionar con Django - recibe datos desde requests HTTP
en lugar de input() de consola.
"""

from typing import Dict, Any, Optional
from ..utils.yaml_loader import YAMLConfigLoader


class QuotationProcessor:
    """
    Procesador principal de cotizaciones.
    Maneja toda la lógica de cálculo de costos y precios.
    """

    def __init__(self, config_file: str = 'reglas_negocio.yaml'):
        """
        Inicializa el procesador con la configuración YAML.

        Args:
            config_file: Nombre del archivo YAML de configuración
        """
        self.config_loader = YAMLConfigLoader(config_file)
        self.config = self.config_loader.load()

    def calcular_layout(self, datos: Dict[str, float]) -> Dict[str, float]:
        """
        Calcula dimensiones totales del molde incluyendo márgenes.

        Fórmulas:
        largo = 2 + (ancho_marquilla × cantidad_horizontal) + (espacios × (cantidad_horizontal-1))
        alto = 2 + (alto_marquilla × cantidad_vertical) + (espacios × (cantidad_vertical-1))

        Args:
            datos: Diccionario con ancho_cm, alto_cm, espacio_entre_cm,
                   cantidad_horizontal, cantidad_vertical

        Returns:
            Diccionario con largo_total, alto_total, area_total
        """
        largo_total = (2 +
                       (datos['ancho_cm'] * datos['cantidad_horizontal']) +
                       (datos['cantidad_horizontal'] - 1) * datos['espacio_entre_cm'])

        alto_total = (2 +
                      (datos['alto_cm'] * datos['cantidad_vertical']) +
                      (datos['cantidad_vertical'] - 1) * datos['espacio_entre_cm'])

        area_total = largo_total * alto_total

        return {
            'largo_total': round(largo_total),
            'alto_total': round(alto_total),
            'area_total': round(area_total)
        }

    def calcular_gramos_por_area(self, area_cm2: float, tipo: str = "2_mm") -> Dict[str, float]:
        """
        Calcula gramos usando la fórmula: (area_molde * gramos_tabla) / cm2_tabla

        Args:
            area_cm2: Área del molde en cm²
            tipo: Tipo de material (ej: "2_mm", "3_mm", etc.)

        Returns:
            Diccionario con gramos_total y gramos_por_cm2
        """
        tabla = self.config['cotizacion']['tabla_gramos']
        ref = tabla.get(tipo, tabla['default'])

        gramos_total = (area_cm2 * ref['gramos']) / ref['cm2']
        gramos_por_cm2 = gramos_total / area_cm2

        return {
            'gramos_total': round(gramos_total, 2),
            'gramos_por_cm2': round(gramos_por_cm2, 2)
        }

    def calcular_costos_produccion(self, datos: Dict[str, Any],
                                   area_total: float,
                                   gramos_total: float) -> Dict[str, float]:
        """
        Calcula costos de producción basados en área y gramos calculados.

        Args:
            datos: Diccionario con todos los datos de entrada
            area_total: Área total del molde en cm²
            gramos_total: Gramos totales de material

        Returns:
            Diccionario con todos los costos calculados
        """
        cfg = self.config['cotizacion']
        cantidad = datos['cantidad']

        # Cálculo moldes por hora
        tiempo_mora_molde = cfg['tiempos']['tiempo_setup_por_lote_minutos']
        moldes_por_hora = 60 / tiempo_mora_molde if tiempo_mora_molde else 0

        # Valor por troquelada
        valor_por_troquelada = datos.get('valor_por_troquelada', 0)

        # Material: (gramos_por_molde * valor_por_gramo) / cantidad_marquillas_por_molde
        costo_por_gramo = self.config['cotizacion']['constantes']['costo_por_gramo']
        cantidad_marquillas_por_molde = datos['cantidad_horizontal'] * \
            datos['cantidad_vertical']
        valor_material = (gramos_total * costo_por_gramo) / \
            cantidad_marquillas_por_molde

        # Guardar material en datos
        datos['material'] = valor_material

        # Total materiales (material + montaje + medida)
        montaje = datos.get('montaje', 0) or 0
        medida = datos.get('medida', 0) or 0
        total_material = valor_material + montaje + medida
        datos['total_material'] = total_material

        # Total empaquetado (suma de costos de armado)
        armado = datos.get('armado', {})
        total_armado = sum(float(v or 0)
                           for v in armado.values()) if armado else 0
        datos['total_armado'] = total_armado

        # Otros materiales (mo_rubber, numero_plotter, perforada, guillotina)
        otros_mat = datos.get('otros_materiales', {})
        total_otros_materiales = sum(float(v or 0)
                                     for v in otros_mat.values()) if otros_mat else 0
        datos['otros_materiales_total'] = total_otros_materiales

        # Base para cálculo de CIF
        # base = valor_por_troquelada + total_material + otros_materiales + total_empaquetado
        base_para_cif = (valor_por_troquelada +
                         total_material +
                         total_otros_materiales +
                         total_armado)

        # Cálculo CIF (aplicar porcentajes: 8%, 10%, 15%)
        porcentajes_cif = self.config.get(
            'porcentajes', {}).get('cif', [8, 10, 15])
        cifs = {f"cif_{p}": base_para_cif * (p/100) for p in porcentajes_cif}

        admon = base_para_cif * \
            (self.config.get('porcentajes', {}).get('admon', 5)/100)

        # Costo total producción
        costo_total = base_para_cif + sum(cifs.values()) + admon

        # Precios según utilidad
        porcentajes_utilidad = self.config.get(
            'porcentajes', {}).get('utilidad', [45, 28, 17, 11])
        precios_venta = {
            f"precio_utilidad_{p}": costo_total/(1-p/100)
            for p in porcentajes_utilidad
        }

        return {
            'valor_por_troquelada': round(valor_por_troquelada, 2),
            'moldes_por_hora': round(moldes_por_hora, 2),
            'material': round(valor_material, 2),
            'montaje': round(montaje, 2),
            'medida': round(medida, 2),
            'total_material': round(total_material, 2),
            'total_armado': round(total_armado, 2),
            'otros_materiales_total': round(total_otros_materiales, 2),
            **{k: round(v, 2) for k, v in cifs.items()},
            'admon': round(admon, 2),
            'costo_total': round(costo_total, 2),
            **{k: round(v, 2) for k, v in precios_venta.items()}
        }

    def calcular_cotizacion(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método principal que ejecuta el proceso completo de cotización.

        Args:
            datos: Diccionario con todos los datos necesarios:
                - ancho_cm: float
                - alto_cm: float
                - espacio_entre_cm: float
                - cantidad_horizontal: int
                - cantidad_vertical: int
                - cantidad: int
                - valor_por_troquelada: float
                - montaje: float
                - medida: float
                - armado: dict con costos de armado
                - espesor: str (opcional, default "2_mm")

        Returns:
            Diccionario completo con todos los resultados de la cotización
        """
        try:
            # 1. Calcular dimensiones y área del molde
            dimensiones = self.calcular_layout(datos)
            area_total = dimensiones['area_total']

            # 2. Calcular gramos según área
            espesor = datos.get('espesor', '2_mm')
            gramos = self.calcular_gramos_por_area(area_total, espesor)

            # 3. Calcular costos de producción (incluye base_cif con la fórmula correcta)
            costos = self.calcular_costos_produccion(
                datos, area_total, gramos['gramos_total'])

            # 4. Obtener costo_por_gramo para mostrar
            costo_por_gramo = self.config['cotizacion']['constantes']['costo_por_gramo']

            # 5. Retornar resultado completo
            return {
                'success': True,
                'dimensiones': dimensiones,
                'area_total': area_total,
                'gramos': gramos,
                'costo_por_gramo': costo_por_gramo,
                'costos': costos,
                'datos_entrada': datos
            }

        except KeyError as e:
            return {
                'success': False,
                'error': f'Falta el campo requerido: {str(e)}',
                'error_type': 'missing_field'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al calcular cotización: {str(e)}',
                'error_type': 'calculation_error'
            }


# Funciones standalone para compatibilidad con scripts legacy
# (Internamente usan QuotationProcessor)
_processor_instance = None


def _get_processor():
    """Helper para obtener instancia singleton del processor."""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = QuotationProcessor()
    return _processor_instance


def calcular_layout(datos: Dict[str, float]) -> Dict[str, float]:
    """Wrapper standalone para calcular_layout."""
    return _get_processor().calcular_layout(datos)


def calcular_gramos_por_area(area_cm2: float, config: Dict[str, Any], tipo: str = "2_mm") -> Dict[str, float]:
    """Wrapper standalone para calcular_gramos_por_area."""
    return _get_processor().calcular_gramos_por_area(area_cm2, tipo)


def calcular_costos_produccion(datos: Dict[str, Any],
                               config: Dict[str, Any],
                               area_total: float,
                               gramos_total: float) -> Dict[str, float]:
    """Wrapper standalone para calcular_costos_produccion."""
    return _get_processor().calcular_costos_produccion(datos, area_total, gramos_total)


def main():
    """
    Función principal para ejecutar desde consola (modo standalone).
    Mantiene compatibilidad con el script original.
    """
    print("\n=== INGRESE LOS DATOS DE LA MARQUILLA ===")

    # Solicitar dimensiones y cantidades
    try:
        datos = {
            'ancho_cm': float(input("Ancho de la marquilla (cm): ")),
            'alto_cm': float(input("Alto de la marquilla (cm): ")),
            'espacio_entre_cm': float(input("Espacio entre marquillas (cm): ")),
            'cantidad_horizontal': int(input("Cantidad de marquillas horizontales: ")),
            'cantidad_vertical': int(input("Cantidad de marquillas verticales: ")),
            'cantidad': int(input("Cantidad total a producir: ")),
            'valor_por_troquelada': float(input("Valor por troquelada: "))
        }

        print("\n=== COSTOS DE MATERIAL ===")
        datos['montaje'] = float(input("Valor del montaje: "))
        datos['medida'] = float(input("Valor de la medida: "))

        print("\n=== COSTOS DE ARMADO ===")
        datos['armado'] = {
            'bolsa_individual': float(input("Costo bolsa individual: ")),
            'sellada': float(input("Costo sellado: ")),
            'cortada': float(input("Costo corte: ")),
            'empaque_final': float(input("Costo empaque final: ")),
            'llenada_gel': float(input("Costo llenado gel: ")),
            'pin_soporte': float(input("Costo pin soporte: ")),
            'samblasted': float(input("Costo samblasted: "))
        }

    except ValueError as e:
        print("\nError: Por favor ingrese números válidos")
        return

    # Usar la clase QuotationProcessor
    processor = QuotationProcessor()
    resultado = processor.calcular_cotizacion(datos)

    if not resultado['success']:
        print(f"\n❌ Error: {resultado['error']}")
        return

    # Extraer datos del resultado
    dimensiones = resultado['dimensiones']
    gramos = resultado['gramos']
    costos = resultado['costos']

    # Imprimir resultados
    print("\n=== COTIZACIÓN DETALLADA ===")
    print(
        f"Dimensiones del molde: {dimensiones['largo_total']}cm x {dimensiones['alto_total']}cm")
    print(f"Área total: {resultado['area_total']} cm²")
    print(f"Gramos totales: {gramos['gramos_total']}g")
    print(f"Gramos por cm²: {gramos['gramos_por_cm2']}g")
    print(f"Costo por gramo: ${resultado['costo_por_gramo']:,.2f}")

    print("\nCOSTOS DE MATERIAL:")
    print(f"Material (por unidad): ${resultado['valor_material']:,.2f}")
    print(f"Montaje: ${datos['montaje']:,.2f}")
    print(f"Medida: ${datos['medida']:,.2f}")
    print(f"Total Material: ${resultado['total_material']:,.2f}")

    print("\nCOSTOS DE ARMADO:")
    for concepto, valor in datos['armado'].items():
        print(f"{concepto}: ${valor:,.2f}")
    print(f"Total Armado: ${resultado['total_armado']:,.2f}")

    print("\nCOSTOS DE PRODUCCIÓN:")
    for k, v in costos.items():
        if isinstance(v, (int, float)):
            if 'costo' in k or 'precio' in k:
                print(f"{k}: ${v:,.2f}")
            else:
                print(f"{k}: {v:.2f}")


if __name__ == "__main__":
    main()
