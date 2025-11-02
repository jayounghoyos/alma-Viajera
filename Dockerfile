# Imagen base oficial de Python
FROM python:3.10-slim

# Variables de entorno básicas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Crear carpetas necesarias
RUN mkdir -p /app/staticfiles /app/media

#  Recopilar los archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer el puerto (Cloud Run usa PORT env variable)
EXPOSE 8080

#  Iniciar el servidor con gunicorn (usa whitenoise internamente)
# Cloud Run inyecta PORT automáticamente
CMD exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3
