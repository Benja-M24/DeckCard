# Development stage
FROM python:3.12.1 AS development
# Configurar el directorio de trabajo
WORKDIR /usr/src/app
# Copiar los archivos de requerimientos
COPY requirements.txt .
# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
# Copiar el resto del proyecto
# COPY ./API .
# Crear el proyecto Django (este comando solo se ejecutará la primera vez)
RUN django-admin startproject DeckCard
# Exponer el puerto para el servidor Django
EXPOSE 8800
# Comando por defecto para iniciar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8800"]


# Build stage


# # Production stage
# pip install gunicorn
# # Iniciar el servidor en producción
# gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 4
FROM python:3.12.1-slim AS production
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8800
CMD ["gunicorn", "DeckCard.wsgi:application", "--bind", "0.0.0.0:8800"]