# dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

# Instalar dependencias del sistema necesarias para Chromium/Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    gnupg \
    lsb-release \
    fonts-liberation \
    fonts-noto-color-emoji \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libx11-xcb1 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libxss1 \
    libasound2 \
    libxshmfence1 \
    libdrm2 \
 && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Instalar navegadores de Playwright (y sus dependencias si faltan)
# Esto descarga Chromium (u otros navegadores) al path definido en PLAYWRIGHT_BROWSERS_PATH
RUN python -m playwright install --with-deps

# Crear carpetas necesarias y recopilar estáticos
RUN mkdir -p /app/staticfiles /app/media /ms-playwright
RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3
