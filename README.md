# Alma Viajera

Alma viajera es un e-commerce donde hacemos reservas de servicios turísticos, ayudando no solo a los grandes y clásicos servicios turísticos sino también a los pequeños empredimientos y servicios que de otra manera podrían pasar desapercibidos y que ¡incluso! representan al lugar que estas visitando.
![WhatsApp Image 2025-11-03 at 4 56 09 PM](https://github.com/user-attachments/assets/18e610f6-b33e-4967-963e-2d43c9ed8859)

## Características

- **Mapa interactivo** para selección de países
- **Catálogo de servicios** por categorías (Lugares, Tours, Comida, Actividades, Souvenirs)
- **Sistema de carrito** de compras
- **Panel de proveedores** para gestión de servicios
- **Sistema de autenticación** diferenciado (Clientes vs Proveedores)
- **Búsqueda y filtros** avanzados
- **Diseño responsive** con Bootstrap 5

## Requisitos del Sistema

- Python 3.8+
- Django 5.2.5
- SQLite3 

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd alma-Viajera
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

```bash
python manage.py migrate
```

### 5. Crear datos de muestra (opcional)

```bash
python manage.py create_sample_data
```

Este comando creará:
- 5 categorías de servicios
- 1 usuario vendedor de prueba (usuario: `vendedor_test`, contraseña: `test123`)
- 6 items de muestra (uno por país)

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

El proyecto estará disponible en `http://127.0.0.1:8000/`

## Estructura del Proyecto

```
alma-Viajera/
├── apps/
│   ├── core/           # Página principal y navegación
│   ├── catalog/        # Catálogo de servicios turísticos
│   ├── cart/           # Carrito de compras
│   ├── user/           # Autenticación y gestión de usuarios
│   ├── providers/      # Panel para proveedores de servicios
│   ├── order/          # Gestión de reservas y pagos
│   └── review/         # Sistema de reseñas
├── config/             # Configuración principal de Django
├── templates/          # Templates base
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── media/              # Archivos subidos por usuarios
└── manage.py
```

## Uso del Sistema

### Para Usuarios

1. **Explorar por Mapa**: Accede a `/mapa/` para seleccionar un país
2. **Explorar Catálogo**: Navega por categorías y filtra por país
3. **Buscar Servicios**: Usa la barra de búsqueda para encontrar servicios específicos
4. **Agregar al Carrito**: Selecciona servicios y gestiona tu carrito
5. **Crear Cuenta**: Regístrate como cliente o proveedor

### Para Proveedores

1. **Registrarse**: Crear cuenta como proveedor
2. **Panel de Control**: Acceder a `/providers/account/`
3. **Crear Servicios**: Publicar tours, actividades, etc.
4. **Gestionar Servicios**: Editar, eliminar o ver estadísticas

## Países Disponibles

- Colombia
- México
- Argentina
- Perú
- Chile
- Brasil

## Categorías de Servicios

- **Lugares**: Destinos turísticos y puntos de interés
- **Tours**: Recorridos guiados
- **Comida**: Experiencias culinarias
- **Actividades**: Aventuras y experiencias
- **Souvenirs**: Productos locales

## Comandos de Gestión

### Crear datos de muestra
```bash
python manage.py create_sample_data
```

### Limpiar base de datos
```bash
python manage.py flush
```

### Crear migraciones
```bash
python manage.py makemigrations
```

### Aplicar migraciones
```bash
python manage.py migrate
```

## Configuración de Desarrollo

### Variables de Entorno

El proyecto usa configuración por defecto para desarrollo. Para producción, configura:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- Base de datos de producción

### Archivos Estáticos

```bash
python manage.py collectstatic
```

### Archivos de Media

Los archivos subidos se guardan en la carpeta `media/` y se sirven automáticamente en desarrollo.

## Tecnologías Utilizadas

- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5, HTMX, Leaflet.js
- **Base de Datos**: SQLite3
- **Mapas**: OpenStreetMap
- **Iconos**: Bootstrap Icons

## Estructura de la Base de Datos

### Modelos Principales

- **Usuario**: Sistema de usuarios personalizado con roles
- **Item**: Servicios turísticos
- **Categoria**: Categorías de servicios
- **Carrito**: Carrito de compras del usuario
- **Reserva**: Reservas de servicios
- **Review**: Sistema de reseñas

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas sobre el proyecto, contacta al equipo de desarrollo.

## Changelog

### v1.0.0
- Implementación inicial del sistema
- Mapa interactivo de países
- Catálogo de servicios
- Sistema de carrito
- Panel de proveedores
- Autenticación de usuarios
