# Create
FROM node:20.18.1 AS create
WORKDIR /usr/src/app/deckcard-ui
COPY deckcard-ui/package*.json ./
RUN npm install
# docker compose run --rm --entrypoint sh frontend
# cd /usr/src/app 
# npm create astro@latest

# Development stage
FROM node:20.18.1 AS development
# Create and set working directory
WORKDIR /usr/src/app/deckcard-ui

# Copiar primero solo package.json y package-lock.json para optimizar la capa de Docker
COPY deckcard-ui/package*.json ./

# Instalar explícitamente @astrojs/react antes de las demás dependencias 
# para asegurar que se instale correctamente
RUN npm cache clean --force && \
    npm install @astrojs/react --no-fund --no-audit && \
    npm install react react-dom --no-fund --no-audit && \
    npm install --no-fund --no-audit

# Verificar la instalación de dependencias críticas
RUN npm list @astrojs/react react react-dom || true

# Copiar el resto de archivos del proyecto
COPY deckcard-ui/ .

# Default command to start Astro in development
CMD ["npm", "run", "dev"]

# Builder stage
FROM node:20.18.1 AS builder
# Create and set working directory
WORKDIR /usr/src/app/deckcard-ui

# Copiar primero solo package.json y package-lock.json para optimizar la capa de Docker
COPY deckcard-ui/package*.json ./

# Instalar explícitamente @astrojs/react antes de las demás dependencias
# Esto asegura que se instale correctamente sin conflictos
RUN npm cache clean --force && \
    npm install @astrojs/react --no-fund --no-audit && \
    npm install react react-dom --no-fund --no-audit && \
    npm install --no-fund --no-audit

# Verificar la instalación de dependencias críticas
RUN npm list @astrojs/react react react-dom || true

# Copiar el resto de archivos del proyecto
COPY deckcard-ui/ .

# Build the project
RUN npm run build

# Production stage
FROM nginx:alpine AS production
# Copy build files
COPY --from=builder /usr/src/app/deckcard-ui/dist /usr/share/nginx/html
# Configuración para manejar rutas de Astro con i18n
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Start Nginx
CMD ["nginx", "-g", "daemon off;"]