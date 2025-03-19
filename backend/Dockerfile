# Debug method
# docker compose run --rm --entrypoint bash backend

# Development stage
FROM python:3.12.1 AS development
# Configurar el directorio de trabajo
WORKDIR /usr/src/app
# Copiar los archivos de requerimientos
COPY requirements.txt .
# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
# Copiar el resto del proyecto
COPY ./API .
# Ejecutar migraciones
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# Comando por defecto para iniciar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8800"]

# Production stage
FROM python:3.12.1-slim AS production
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8800
CMD ["gunicorn", "API.wsgi:application", "--bind", "0.0.0.0:8800", "--workers", "4"]