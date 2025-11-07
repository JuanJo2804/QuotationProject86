# 📘 Documentación de Integración - Sistema de Cotización

## ✅ Resumen de la Integración

Se ha integrado exitosamente el archivo `main_re.py` (lógica de cotización) en el proyecto Django siguiendo las mejores prácticas de arquitectura de software.

---

## 📁 Estructura Creada

```
quotations/
├── business_logic/                 # Lógica de negocio (independiente de Django)
│   ├── __init__.py
│   └── quotation_processor.py     # Tu main_re.py refactorizado
│
├── config/                         # Archivos de configuración
│   └── reglas_negocio.yaml        # Reglas de negocio en YAML
│
├── forms/                          # Formularios Django
│   ├── __init__.py
│   └── quotation_form.py          # Formulario web para cotización
│
├── utils/                          # Utilidades reutilizables
│   ├── __init__.py
│   └── yaml_loader.py             # Loader de archivos YAML
│
├── templates/
│   └── paginas/
│       └── cotizacion.html        # Interface web
│
├── views.py                        # Vistas Django (adaptadas)
├── urls.py                         # Rutas
└── models.py                       # Modelos (futuro)
```

---

## 🔄 Cambios Realizados

### 1. **quotation_processor.py** (antes main_re.py)

**Cambios principales:**

- ✅ Convertido a **clase orientada a objetos** (`QuotationProcessor`)
- ✅ Eliminados `input()` de consola
- ✅ Método `calcular_cotizacion()` recibe diccionario de datos
- ✅ Retorna resultados estructurados (dict con `success`, `error`, datos)
- ✅ Usa `YAMLConfigLoader` para cargar configuración
- ✅ Mantiene compatibilidad con modo consola mediante función `main()`

**Uso desde Django:**

```python
from quotations.business_logic.quotation_processor import QuotationProcessor

processor = QuotationProcessor()
resultado = processor.calcular_cotizacion(datos)
```

**Uso desde consola (standalone):**

```bash
python quotations/business_logic/quotation_processor.py
```

---

### 2. **yaml_loader.py** (nuevo)

Utilidad para cargar archivos YAML de forma robusta.

**Características:**

- ✅ Busca automáticamente en `quotations/config/` y raíz del proyecto
- ✅ Cachea la configuración (no recarga en cada llamada)
- ✅ Soporta claves anidadas con notación de punto (`config.get('cotizacion.constantes.costo_por_gramo')`)
- ✅ Manejo de errores descriptivo

---

### 3. **quotation_form.py** (nuevo)

Formulario Django para recibir datos desde el navegador.

**Campos incluidos:**

- Dimensiones (ancho, alto, espacio)
- Cantidades (horizontal, vertical, total)
- Costos (troquelada, montaje, medida)
- Armado (7 opciones opcionales)
- Material (tipo seleccionable)

**Método útil:**

```python
form = QuotationForm(request.POST)
if form.is_valid():
    datos = form.get_datos_cotizacion()  # Formatea para processor
```

---

### 4. **views.py** (actualizado)

**Vista `cotizacion`:**

```python
def cotizacion(request):
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            datos = form.get_datos_cotizacion()
            processor = QuotationProcessor()
            resultado = processor.calcular_cotizacion(datos)
    return render(request, 'paginas/cotizacion.html', {'form': form, 'resultado': resultado})
```

**Características:**

- ✅ Maneja GET (muestra formulario) y POST (procesa)
- ✅ Soporta respuestas AJAX/JSON
- ✅ Pasa resultados al template

---

### 5. **cotizacion.html** (creado)

Template completo con Tailwind CSS.

**Secciones:**

- Formulario de entrada (lado izquierdo)
- Resultados de cotización (lado derecho)
- Diseño responsive (grid layout)
- Validación de errores
- Formateo de números

---

## 🚀 Cómo Usar el Sistema

### **Opción 1: Desde el Navegador**

1. Iniciar servidor:

```bash
python manage.py runserver
```

2. Abrir en el navegador:

```
http://127.0.0.1:8000/cotizacion
```

3. Completar el formulario y hacer clic en "Calcular Cotización"

---

### **Opción 2: Desde Consola (Modo Legacy)**

```bash
python quotations/business_logic/quotation_processor.py
```

---

### **Opción 3: Programático (Desde código Python)**

```python
from quotations.business_logic.quotation_processor import QuotationProcessor

# Datos de ejemplo
datos = {
    'ancho_cm': 4,
    'alto_cm': 3,
    'espacio_entre_cm': 0.5,
    'cantidad_horizontal': 10,
    'cantidad_vertical': 10,
    'cantidad': 1000,
    'valor_por_troquelada': 100,
    'montaje': 500,
    'medida': 200,
    'armado': {
        'bolsa_individual': 0,
        'sellada': 0,
        'cortada': 0,
        'empaque_final': 0,
        'llenada_gel': 0,
        'pin_soporte': 0,
        'samblasted': 0,
    }
}

processor = QuotationProcessor()
resultado = processor.calcular_cotizacion(datos)

if resultado['success']:
    print(f"Costo total: ${resultado['costos']['costo_total']}")
else:
    print(f"Error: {resultado['error']}")
```

---

## 📦 Dependencias Instaladas

```bash
pip install pyyaml  # Para leer archivos YAML
```

---

## 🧪 Testing

### **Verificar que el YAML se carga correctamente:**

```python
from quotations.utils.yaml_loader import YAMLConfigLoader

loader = YAMLConfigLoader('reglas_negocio.yaml')
config = loader.load()
print(config['cotizacion']['constantes']['costo_por_gramo'])  # Debe imprimir 29
```

### **Probar el processor:**

```python
from quotations.business_logic.quotation_processor import QuotationProcessor

processor = QuotationProcessor()
print(processor.config['cotizacion']['constantes'])  # Ver configuración
```

---

## 🔐 Seguridad y Mejores Prácticas

✅ **Separación de responsabilidades:**

- Business logic NO depende de Django
- Puede ser reutilizada en otros proyectos

✅ **Validación de datos:**

- Django Forms valida inputs antes de procesar
- QuotationProcessor maneja errores gracefully

✅ **Configuración externa:**

- Reglas de negocio en YAML (fácil de modificar sin tocar código)

✅ **Modularidad:**

- Cada componente tiene una responsabilidad única
- Fácil de testear y mantener

---

## 🎯 Próximos Pasos Recomendados

### **Corto plazo:**

1. ✅ Crear modelos Django para guardar cotizaciones en BD
2. ✅ Agregar autenticación de usuarios
3. ✅ Historial de cotizaciones
4. ✅ Exportar resultados a PDF

### **Mediano plazo:**

1. ✅ API REST (Django REST Framework)
2. ✅ Tests unitarios
3. ✅ Panel de administración personalizado
4. ✅ Reportes y estadísticas

---

## 📝 Notas Importantes

### **Modificar las reglas de negocio:**

Editar: `quotations/config/reglas_negocio.yaml`

### **Agregar nuevos campos al formulario:**

1. Agregar campo en `quotation_form.py`
2. Actualizar `get_datos_cotizacion()`
3. Actualizar template `cotizacion.html`

### **Modificar cálculos:**

Editar métodos en `QuotationProcessor` en `quotation_processor.py`

---

## 🐛 Troubleshooting

**Error: "FileNotFoundError: reglas_negocio.yaml"**

- Verificar que el archivo esté en `quotations/config/`

**Error: "Import yaml could not be resolved"**

- Ejecutar: `pip install pyyaml`

**El formulario no muestra estilos:**

- Verificar que Tailwind CSS esté compilado
- Ejecutar: `npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch`

**Los cálculos no son correctos:**

- Verificar valores en `reglas_negocio.yaml`
- Revisar fórmulas en `quotation_processor.py`

---

## 👥 Autor

**JuanJo2804**

- GitHub: [@JuanJo2804](https://github.com/JuanJo2804)

---

## 📅 Fecha de Integración

Noviembre 7, 2025

---

¡La integración está completa y lista para usar! 🎉
