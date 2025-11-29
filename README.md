# QuotationProject86

Sistema integral de gestión de cotizaciones para productos de impresión y troquelado, desarrollado con Django y Tailwind CSS.

## 📋 Descripción

QuotationProject86 es una aplicación web completa diseñada para gestionar cotizaciones de productos de impresión y troquelado. El sistema incluye cálculo automático de costos, gestión de clientes, seguimiento de estados de cotizaciones, y generación de PDFs. El proyecto está construido con Django 5.2.6 en el backend y utiliza Tailwind CSS 4 para el diseño frontend moderno y responsivo.

## ✨ Características Principales

- 📊 **Cálculo Automático de Cotizaciones**: Sistema inteligente que calcula costos de material, armado, CIF, administración y precios de venta con diferentes márgenes de utilidad
- 👥 **Gestión de Clientes**: CRUD completo para administrar información de clientes (nombre, correo, teléfono, dirección)
- 📈 **Estados de Cotizaciones**: Seguimiento del flujo de trabajo con estados: Pendiente, Enviada, Aprobada
- 🔍 **Filtros Avanzados**: Búsqueda por cliente, estado y fecha de creación
- 📄 **Generación de PDFs**: Exportación de cotizaciones detalladas en formato PDF con ReportLab
- 🎨 **Interfaz Moderna**: Diseño responsivo con Tailwind CSS y componentes interactivos
- 📱 **Responsive Design**: Optimizado para desktop, tablet y móvil
- 🔐 **Sistema de Autenticación**: Gestión de usuarios y permisos integrado

## 🚀 Tecnologías

- **Backend:** Django 5.2.6
- **Frontend:** Tailwind CSS 4.1.16
- **Base de datos:** PostgreSQL
- **Python:** 3.14+
- **API:** Django REST Framework
- **PDF Generation:** ReportLab
- **Node.js:** Para gestión de paquetes de Tailwind

## 📁 Estructura del Proyecto

```
QuotationProject86/
├── quotation_project/          # Configuración principal del proyecto Django
│   ├── settings.py             # Configuración de Django (PostgreSQL, apps, middleware)
│   ├── urls.py                 # URLs principales del proyecto
│   ├── wsgi.py                 # Configuración WSGI para deployment
│   └── asgi.py                 # Configuración ASGI para async
├── quotations/                 # Aplicación principal de cotizaciones
│   ├── models.py               # Modelo Quotation con cálculos y estados
│   ├── views.py                # Vistas para CRUD y cálculo de cotizaciones
│   ├── urls.py                 # URLs de la app quotations
│   ├── forms/                  # Formularios de cotización
│   │   └── quotation_form.py
│   ├── business_logic/         # Lógica de negocio
│   │   └── quotation_processor.py
│   ├── utils/                  # Utilidades
│   │   ├── yaml_loader.py
│   │   └── pdf_generator.py    # Generación de PDFs
│   ├── config/                 # Configuraciones
│   │   └── reglas_negocio.yaml
│   ├── templates/              # Plantillas HTML
│   │   └── paginas/
│   │       ├── cotizaciones.html
│   │       ├── lista_cotizaciones.html
│   │       └── eliminar_cotizacion.html
│   └── migrations/             # Migraciones de base de datos
├── interfaz_crud/              # Aplicación de gestión de clientes
│   ├── models.py               # Modelo Cliente
│   ├── views.py                # Vistas para CRUD de clientes
│   ├── urls.py                 # URLs de la app interfaz_crud
│   ├── forms.py                # Formularios de cliente
│   ├── templates/              # Plantillas HTML
│   │   └── interfaz_crud/
│   │       ├── inicio.html
│   │       ├── cliente_list.html
│   │       ├── cliente_form.html
│   │       ├── cliente_confirm_delete.html
│   │       └── base.html
│   └── migrations/             # Migraciones de base de datos
├── Filterss/                   # Formularios de filtros (deprecated)
│   └── quotation_filter_form.py
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── output.css          # CSS compilado de Tailwind
│   ├── src/
│   │   └── input.css           # CSS fuente de Tailwind
│   └── images/                 # Imágenes del proyecto
├── cotizaciones_pdf/           # PDFs generados (creado automáticamente)
├── venv/                       # Entorno virtual de Python
├── node_modules/               # Dependencias de Node.js
├── docs/                       # Documentación del proyecto
│   └── PROJECT_DOCUMENTATION.md
├── manage.py                   # Script de gestión de Django
├── tailwind.config.js          # Configuración de Tailwind CSS
├── package.json                # Dependencias de npm
└── README.md                   # Este archivo
```

## 🔧 Instalación

### Prerrequisitos

- Python 3.11 o superior
- Node.js y npm
- Git

### Pasos de instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/JuanJo2804/QuotationProject86.git
   cd QuotationProject86
   ```

2. **Crear y activar entorno virtual**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias de Python**

   ```bash
   pip install django==5.2.6
   pip install psycopg2-binary      # Para PostgreSQL
   pip install djangorestframework  # Django REST Framework
   pip install pyyaml              # Para configuración YAML
   pip install reportlab           # Para generación de PDFs
   ```

4. **Instalar dependencias de Node.js**

   ```bash
   npm install
   ```

5. **Configurar PostgreSQL**

   Crear la base de datos y usuario:

   ```sql
   CREATE DATABASE crud_quotation;
   CREATE USER quotation_admin WITH PASSWORD '123';
   ALTER ROLE quotation_admin SET client_encoding TO 'utf8';
   ALTER ROLE quotation_admin SET default_transaction_isolation TO 'read committed';
   ALTER ROLE quotation_admin SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE crud_quotation TO quotation_admin;
   ```

   La configuración en `settings.py` ya está lista:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'crud_quotation',
           'USER': 'quotation_admin',
           'PASSWORD': '123',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. **Aplicar migraciones**

   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**

   ```bash
   python manage.py createsuperuser
   ```

7. **Compilar Tailwind CSS**
   ```bash
   npx @tailwindcss/cli -i ./static/src/input.css -o ./static/css/output.css --watch
   ```

## 🖥️ Uso

### Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

### URLs principales

- Página principal: `http://127.0.0.1:8000/`
- Gestión de clientes: `http://127.0.0.1:8000/interfaz_crud/clientes/`
- Crear cotización: `http://127.0.0.1:8000/quotations/calcular/`
- Lista de cotizaciones: `http://127.0.0.1:8000/quotations/lista/`
- Panel de administración: `http://127.0.0.1:8000/admin/`

### Flujo de trabajo

1. **Gestión de Clientes**
   - Crear, editar y eliminar clientes desde la interfaz CRUD
   - Campos requeridos: nombre, correo electrónico, teléfono, dirección

2. **Crear Cotización**
   - Seleccionar un cliente existente
   - Ingresar dimensiones del producto (largo × ancho × altura en cm)
   - Especificar cantidad de productos
   - Hacer clic en **Calcular** para obtener costos y tiempo de producción
   - Hacer clic en **Guardar** para almacenar la cotización
   - Usar **Generar PDF** para descargar el documento

3. **Gestión de Estados**
   - Cada cotización tiene uno de tres estados:
     - 🟡 **Pendiente**: Cotización recién creada
     - 🔵 **Enviada**: Cotización enviada al cliente
     - 🟢 **Aprobada**: Cotización aprobada
   - Cambiar estado con el botón de ciclo: Pendiente → Enviada → Aprobada → Pendiente

4. **Filtros**
   - Filtrar por estado en la lista de cotizaciones
   - Filtrar por rango de fechas (desde/hasta)
   - Combinar ambos filtros para búsquedas específicas

### Comandos útiles

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test

# Compilar Tailwind CSS (watch mode)
npm run watch
```

## 🗄️ Base de Datos

El proyecto utiliza **PostgreSQL** como base de datos principal.

### Configuración actual

Base de datos: `crud_quotation`  
Usuario: `quotation_admin`  
Host: `localhost`  
Puerto: `5432`

### Estructura de tablas principales

- **quotations_quotation**: Almacena las cotizaciones con dimensiones, costos y estado
- **interfaz_crud_cliente**: Información de clientes (nombre, correo, teléfono, dirección)

### Modelos

**Quotation** (quotations/models.py):
```python
- client: ForeignKey a Cliente
- largo, ancho, altura: DecimalField (dimensiones en cm)
- cantidad: IntegerField
- costo_total: DecimalField
- tiempo_produccion: IntegerField (días)
- estado: CharField (pendiente/enviada/aprobada)
- fecha_cotizacion: DateTimeField
```

**Cliente** (interfaz_crud/models.py):
```python
- nombre: CharField
- correo_electronico: EmailField
- telefono: CharField
- direccion: TextField
```

### Migraciones importantes

El proyecto ha aplicado todas las migraciones necesarias, incluyendo:
- Creación de modelos base
- Agregado del campo `telefono` a Cliente
- Agregado del campo `direccion` a Cliente
- Agregado del campo `estado` a Quotation con tres opciones
```

## 🎨 Tailwind CSS

El proyecto utiliza Tailwind CSS 4. Para compilar los estilos:

```bash
# Modo desarrollo (con watch)
npx @tailwindcss/cli -i ./static/src/input.css -o ./static/css/output.css --watch

# Modo producción (optimizado)
npx @tailwindcss/cli -i ./static/src/input.css -o ./static/css/output.css --minify
```

## 📋 Funcionalidades Detalladas

### Sistema de Estados
Las cotizaciones pueden tener tres estados diferentes:

1. **Pendiente** 🟡
   - Estado inicial al crear una cotización
   - Indica que la cotización aún no ha sido enviada al cliente

2. **Enviada** 🔵
   - Cotización compartida con el cliente
   - En espera de aprobación

3. **Aprobada** 🟢
   - Cliente ha aceptado la cotización
   - Lista para producción

El cambio de estado es cíclico: se puede avanzar al siguiente estado con un solo clic, facilitando el seguimiento del flujo de trabajo.

### Generación de PDFs
Los PDFs generados incluyen:
- Información completa del cliente
- Dimensiones del producto
- Desglose de costos (materiales, mano de obra, utilidad)
- Tiempo estimado de producción
- Fecha de cotización
- Logo y formato profesional

### Filtros Avanzados
- **Por estado**: Ver solo cotizaciones en un estado específico
- **Por fecha**: Filtrar por rango de fechas (desde/hasta)
- **Combinados**: Aplicar ambos filtros simultáneamente

### Cálculo de Costos
El sistema calcula automáticamente:
- Costo de materiales según dimensiones y cantidad
- Costo de mano de obra
- Margen de utilidad
- Tiempo de producción estimado
- Costo total de la cotización

Los cálculos se basan en reglas de negocio configurables en `quotations/config/reglas_negocio.yaml`.

## 🌿 Estructura de Ramas Git

- `main` - Rama principal estable con todas las características implementadas
- Características actuales en `main`:
  - ✅ Sistema de estados con tres opciones
  - ✅ Generación independiente de PDFs
  - ✅ Filtros por estado y fecha
  - ✅ CRUD completo de clientes
  - ✅ Interfaz optimizada sin scroll horizontal

## 📝 Aplicaciones

### quotations
Aplicación principal para el cálculo y gestión de cotizaciones.

**Características:**
- Cálculo automático de costos basado en dimensiones y cantidad
- Gestión de estados (pendiente, enviada, aprobada)
- Generación de PDFs con información completa de la cotización
- Filtrado por estado y fecha
- Business logic separada en `business_logic/quotation_processor.py`
- Configuración de reglas de negocio en `config/reglas_negocio.yaml`

**Componentes principales:**
- `models.py`: Modelo Quotation con campos de dimensiones, costos y estado
- `views.py`: Vistas para crear, listar, calcular y cambiar estado
- `forms/quotation_form.py`: Formulario personalizado para cotizaciones
- `utils/pdf_generator.py`: Generación de PDFs con ReportLab
- `business_logic/quotation_processor.py`: Lógica de cálculo de costos

### interfaz_crud
Aplicación para la gestión CRUD de clientes.

**Características:**
- CRUD completo de clientes (Crear, Leer, Actualizar, Eliminar)
- Interfaz responsive con Tailwind CSS
- Validación de formularios
- API REST con Django REST Framework

**Componentes principales:**
- `models.py`: Modelo Cliente con información de contacto
- `views.py`: Vistas basadas en clases para CRUD
- `forms.py`: Formularios de cliente
- `serializers.py`: Serializers para API REST
- `api.py` y `urls_api.py`: Endpoints REST para clientes

## 🧪 Testing

El proyecto incluye casos de prueba documentados en `docs/PROJECT_DOCUMENTATION.md`. Los casos de prueba cubren:

### User Story 1: Gestión de Estados de Cotizaciones
- Crear cotización con estado inicial "pendiente"
- Cambiar estado de pendiente a enviada
- Cambiar estado de enviada a aprobada
- Ciclo completo de estado (aprobada vuelve a pendiente)

### User Story 2: Filtrado de Cotizaciones
- Filtrar cotizaciones por estado
- Filtrar cotizaciones por rango de fechas
- Filtros combinados (estado + fecha)
- Reset de filtros

### User Story 3: Generación de PDFs
- Botón PDF deshabilitado sin cálculo previo
- Generar PDF después del cálculo
- Validar contenido del PDF generado

Para ejecutar los tests:
```bash
python manage.py test quotations
python manage.py test interfaz_crud
```

## 🔐 Seguridad

⚠️ **Importante para producción:**

1. **Cambiar SECRET_KEY** en `settings.py` - usar variable de entorno
2. **Establecer DEBUG = False**
3. **Configurar ALLOWED_HOSTS** con dominios permitidos
4. **Usar variables de entorno** para datos sensibles (DB_PASSWORD, SECRET_KEY)
5. **Configurar HTTPS** con certificado SSL/TLS
6. **Actualizar contraseñas** de base de datos (actualmente contraseña de ejemplo: '123')
7. **Implementar CORS** apropiado para API REST
8. **Validar y sanitizar** entradas de usuario

### Variables de entorno recomendadas
```bash
SECRET_KEY=tu_clave_secreta_aqui
DB_NAME=crud_quotation
DB_USER=quotation_admin
DB_PASSWORD=contraseña_segura
DB_HOST=localhost
DB_PORT=5432
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

## 📚 Documentación Adicional

- **Documentación completa del proyecto**: `docs/PROJECT_DOCUMENTATION.md`
- **Integración con sistemas externos**: `INTEGRACION.md`
- **Configuración de reglas de negocio**: `quotations/config/reglas_negocio.yaml`

### Archivos de configuración importantes

- `quotation_project/settings.py` - Configuración principal de Django
- `tailwind.config.js` - Configuración de Tailwind CSS
- `package.json` - Dependencias de Node.js

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

### Guías de contribución

- Seguir el estilo de código existente (PEP 8 para Python)
- Escribir tests para nuevas funcionalidades
- Actualizar documentación cuando sea necesario
- Mantener commits atómicos y descriptivos
- Asegurar que todas las pruebas pasen antes de hacer PR

## 👤 Autor

**JuanJo2804**
**SEBAS126**
**Landero-J24**

- GitHub: [@JuanJo2804](https://github.com/JuanJo2804)

## 📄 Licencia

Este proyecto está bajo la Licencia ISC.

## 📞 Soporte

Para reportar problemas o solicitar nuevas características, por favor abre un issue en:
https://github.com/JuanJo2804/QuotationProject86/issues

---

⭐ Si este proyecto te ha sido útil, considera darle una estrella en GitHub
