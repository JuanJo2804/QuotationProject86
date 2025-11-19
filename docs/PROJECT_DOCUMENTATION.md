# Proyecto: QuotationProject86

Resumen y documentación técnica completa del proyecto.

**Resumen del proyecto:**
- **Nombre:** `QuotationProject86`
- **Descripción breve:** Aplicación Django para gestionar clientes y cotizaciones, con una capa de lógica de negocio separada (cálculo/procesamiento de cotizaciones) y una interfaz CRUD basada en plantillas y APIs REST.

**Tecnologías:**
- **Backend:** Python, Django 5.x
- **APIs:** Django REST Framework (`rest_framework`)
- **DB (desarrollo):** SQLite (archivo `db.sqlite3`)
- **Frontend / CSS:** Tailwind CSS (build con `@tailwindcss/cli`)
- **Gestión de paquetes frontend:** `npm` / `package.json`

**Estructura principal del repo (resumida):**
- `quotation_project/` - configuración Django (settings, urls, wsgi/asgi)
- `interfaz_crud/` - app que contiene modelos `Cliente` y `Cotizacion`, vistas, templates y API
- `quotations/` - app con lógica de negocio, formularios y procesamiento de cotizaciones
- `static/` - archivos estáticos; `static/css/output.css` es el CSS compilado por Tailwind
- `docs/` - documentación del proyecto (este archivo)

**Setup rápido (desarrollo)**

1. Crear y activar entorno virtual (ejemplo macOS/zsh):

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias Python:

```
pip install -r requirements.txt
# si no existe requirements.txt:
pip install django djangorestframework pyyaml
```

3. Instalar dependencias Node (solo si trabajas en frontend/tailwind):

```
npm install
```

4. Compilar Tailwind (modo único o watch):

```
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify
# o para desarrollo con watch:
npx @tailwindcss/cli -i ./static/src/input.css -o ./static/css/output.css --watch
```

5. Migraciones y correr servidor:

```
python manage.py migrate
python manage.py runserver
```

Si ves `You have X unapplied migration(s)` ejecuta `python manage.py migrate`.

**Apps y componentes**

**`interfaz_crud`**
- **Propósito:** Interfaz web (templates + views) para administrar `Cliente` y `Cotizacion`. También expone API endpoints.
- **Modelos principales (archivo `interfaz_crud/models.py`):**
  - `Cliente`:
    - `nombre` (CharField, max_length=255)
    - `correo` (EmailField, unique=True)
    - `telefono` (CharField, opcional)
    - `direccion` (CharField, opcional)
    - `fecha_registro` (DateTimeField, auto_now_add=True)
  - `Cotizacion`:
    - `cliente` (ForeignKey → `Cliente`, related_name='cotizaciones')
    - `fecha_creacion` (DateTimeField, auto_now_add=True)
    - `total` (DecimalField)
    - `descripcion` (TextField, opcional)

- **Vistas/URLs/Templates:**
  - Plantillas en `interfaz_crud/templates/interfaz_crud/` como `cliente_list.html`, `cliente_form.html`, `cotizacion_list.html`, `cotizacion_form.html`, etc.
  - Rutas web en `interfaz_crud/urls.py` y API en `interfaz_crud/urls_api.py`.
  - Serializers y endpoints API en `interfaz_crud/serializers.py` y `interfaz_crud/api.py`.

**`quotations`**
- **Propósito:** Contiene la lógica de negocio para procesar cotizaciones, formularios especializados y reglas (separadas del CRUD). Aquí residen los algoritmos de cálculo, validaciones empresariales y carga de reglas desde YAML.
- **Estructura relevante:**
  - `quotations/business_logic/quotation_processor.py` — funciones o clases que realizan el cálculo de la cotización.
  - `quotations/config/reglas_negocio.yaml` — reglas parametrizables que usa el procesador.
  - `quotations/config/forms/quotation_form.py` — formularios (si aplica) para capturar datos de cotización.
  - Nota: en este proyecto el modelo `Cotizacion` se define en `interfaz_crud` (como fuente única). `quotations` actúa sobre ese modelo vía imports o mediante la API.

**Conexión entre `interfaz_crud` y `quotations`**

- Patrón recomendado (sin duplicar modelos):
  - Mantén el modelo `Cotizacion` en `interfaz_crud` (ya existe). Desde `quotations` importa y usa ese modelo al ejecutar lógica de negocio:

```
# En quotations/business_logic/quotation_processor.py
from interfaz_crud.models import Cotizacion

def procesar_cotizacion(cotizacion_id):
    cot = Cotizacion.objects.get(pk=cotizacion_id)
    # aplicar lógica de negocio y actualizar campos si hace falta
    resultado = {...}
    cot.total = resultado['total']
    cot.save()
    return resultado
```

- Alternativa (extensión sin tocar modelo original): crear un modelo extra con OneToOneField para metadata/ajustes:

```
from django.db import models
from interfaz_crud.models import Cotizacion

class QuotationExtension(models.Model):
    cotizacion = models.OneToOneField(Cotizacion, on_delete=models.CASCADE, related_name='extension')
    processed_at = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
```

- Si necesitas una relación inversa desde `interfaz_crud` hacia objetos específicos del app `quotations`, usa `ForeignKey('quotations.SomeModel', ...)` o `apps.get_model('quotations', 'SomeModel')` para evitar importaciones circulares.

**Serializers y API (ejemplo)**

Ejemplo de serializer para `Cotizacion`:

```
# interfaz_crud/serializers.py
from rest_framework import serializers
from .models import Cotizacion

class CotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = ['id','cliente','fecha_creacion','total','descripcion']
```

Ejemplo de ViewSet y registro en `urls_api.py`:

```
from rest_framework import viewsets
from .models import Cotizacion
from .serializers import CotizacionSerializer

class CotizacionViewSet(viewsets.ModelViewSet):
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer

# urls_api.py
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'cotizaciones', CotizacionViewSet)

urlpatterns = router.urls
```

**Migraciones**
- Mantén las migraciones actualizadas. Antes de correr la app en un nuevo entorno ejecuta:

```
python manage.py makemigrations
python manage.py migrate
```

**Tailwind & assets estáticos**
- `static/src/input.css` es el punto de entrada (con directivas `@tailwind base; @tailwind components; @tailwind utilities;`).
- `static/css/output.css` es el CSS compilado — **no** debe versionarse: añadirlo a `.gitignore` y eliminarlo del índice si ya está trackeado:

```
echo "static/css/output.css" >> .gitignore
git rm --cached static/css/output.css
git commit -m "Stop tracking compiled Tailwind CSS output"
```

- Mantén `package.json` versionado (sí se recomienda commitearlo) porque define dependencias dev.

**.gitignore recomendado (resumen)**

```
# Python
.venv/
*.pyc
__pycache__/

# Node
node_modules/
package-lock.json

# Tailwind compiled output
static/css/output.css

# OS / IDE
.DS_Store
```

**Comandos Git útiles**
- Dejar de trackear archivos generados (ejemplo):

```
git rm -r --cached node_modules
git rm --cached static/css/output.css
git add .gitignore
git commit -m "Añadir .gitignore y dejar de trackear archivos generados"
```

- Si ya se requiere limpiar el historial remoto de archivos grandes: usar `git filter-repo` o BFG (operación avanzada; haz backup antes).

**Despliegue / Producción (puntos clave)**
- Configurar `DATABASES` en `quotation_project/settings.py` para usar PostgreSQL en producción.
- Ejecutar `collectstatic` y configurar un servidor estático (CDN o servidor web) para `STATIC_ROOT`:

```
python manage.py collectstatic
```

- Configurar variables de entorno para `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, y credenciales DB.

**Buenas prácticas y recomendaciones**
- Mantener las reglas de negocio (`quotations/config/reglas_negocio.yaml`) separadas de la lógica de presentación.
- No duplicar modelos entre apps: centraliza `Cotizacion` en `interfaz_crud` y usa importaciones o APIs desde `quotations`.
- Versionar `package.json` pero ignorar artefactos compilados.
- Ejecutar migraciones antes de correr pruebas o servidor.

**Checklist / Próximos pasos**
- [ ] Ejecutar `python manage.py migrate` localmente.
- [ ] Decidir si commitear el `package.json` (recomendado: sí).
- [ ] Ejecutar `git rm --cached static/css/output.css` y commitear para dejar de trackear CSS compilado.
- [ ] Revisar PR y hacer merge cuando el branch esté limpio de artefactos generados.

---

Si quieres que adapte esta documentación a un formato específico (markdown más detallado por app, diagrama ASCII de dependencias, o un archivo `docs/README.md` separado), dime cuál prefieres y lo genero. También puedo crear ejemplos de tests para `quotation_processor` o pipelines de CI/CD.
