# QuotationProject86

Sistema de gestión de cotizaciones desarrollado con Django y Tailwind CSS.

## 📋 Descripción

QuotationProject86 es una aplicación web diseñada para gestionar cotizaciones de manera eficiente. El proyecto está construido con Django 5.2.6 en el backend y utiliza Tailwind CSS 4 para el diseño frontend.

## 🚀 Tecnologías

- **Backend:** Django 5.2.6
- **Frontend:** Tailwind CSS 4.1.16
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Python:** 3.11.9
- **Node.js:** Para gestión de paquetes de Tailwind

## 📁 Estructura del Proyecto

```
QuotationProject86/
├── quotation_project/      # Configuración principal del proyecto Django
│   ├── settings.py         # Configuración de Django
│   ├── urls.py            # URLs principales
│   ├── wsgi.py            # Configuración WSGI
│   └── asgi.py            # Configuración ASGI
├── quotations/            # Aplicación principal de cotizaciones
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas
│   ├── urls.py            # URLs de la app
│   ├── admin.py           # Configuración del admin
│   ├── templates/         # Plantillas HTML
│   └── migrations/        # Migraciones de base de datos
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── venv/                  # Entorno virtual de Python
├── node_modules/          # Dependencias de Node.js
├── manage.py              # Script de gestión de Django
├── tailwind.config.js     # Configuración de Tailwind CSS
├── package.json           # Dependencias de npm
└── README.md             # Este archivo

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
   pip install psycopg2-binary  # Para PostgreSQL
   ```

4. **Instalar dependencias de Node.js**

   ```bash
   npm install
   ```

5. **Configurar la base de datos**

   Para desarrollo (SQLite - por defecto):

   ```bash
   python manage.py migrate
   ```

   Para producción (PostgreSQL):

   - Editar `quotation_project/settings.py`
   - Configurar las credenciales de PostgreSQL en `DATABASES`
   - Ejecutar migraciones: `python manage.py migrate`

6. **Crear superusuario**

   ```bash
   python manage.py createsuperuser
   ```

7. **Compilar Tailwind CSS**
   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch
   ```

## 🖥️ Uso

### Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

El proyecto estará disponible en: `http://127.0.0.1:8000/`

Panel de administración: `http://127.0.0.1:8000/admin/`

### Comandos útiles

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear una nueva aplicación
python manage.py startapp nombre_app

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

## 🗄️ Configuración de Base de Datos

### SQLite (Desarrollo)

Configuración por defecto, no requiere configuración adicional.

### PostgreSQL (Producción)

Editar `quotation_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quotation_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎨 Tailwind CSS

El proyecto utiliza Tailwind CSS 4. Para compilar los estilos:

```bash
# Modo desarrollo (con watch)
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch

# Modo producción (optimizado)
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify
```

## 🌿 Ramas

- `main` - Rama principal estable
- `modulo_quotations` - Rama de desarrollo del módulo de cotizaciones
- `rama_prueba` - Rama para pruebas

## 📝 Aplicaciones Instaladas

- `django.contrib.admin` - Panel de administración
- `django.contrib.auth` - Sistema de autenticación
- `django.contrib.contenttypes` - Framework de tipos de contenido
- `django.contrib.sessions` - Framework de sesiones
- `django.contrib.messages` - Framework de mensajes
- `django.contrib.staticfiles` - Gestión de archivos estáticos
- `quotations` - Aplicación principal de cotizaciones

## 🔐 Seguridad

⚠️ **Importante para producción:**

1. Cambiar `SECRET_KEY` en `settings.py`
2. Establecer `DEBUG = False`
3. Configurar `ALLOWED_HOSTS` apropiadamente
4. Usar variables de entorno para datos sensibles
5. Configurar HTTPS

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👤 Autor

**JuanJo2804**

- GitHub: [@JuanJo2804](https://github.com/JuanJo2804)

## 📄 Licencia

Este proyecto está bajo la Licencia ISC.

## 📞 Soporte

Para reportar problemas o solicitar nuevas características, por favor abre un issue en:
https://github.com/JuanJo2804/QuotationProject86/issues

---

⭐ Si este proyecto te ha sido útil, considera darle una estrella en GitHub
