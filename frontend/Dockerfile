# Development stage
FROM node:20.18.1 AS development
# Create and set working directory
WORKDIR /usr/src/app/UI
# Copy configuration files
COPY UI/package*.json ./
# Install project dependencies
RUN npm install
# Copy project files
COPY UI/ .
# Default command to start Astro in development
CMD ["npm", "run", "dev"]

# Builder stage
FROM node:20.18.1 AS builder
# Create and set working directory
WORKDIR /usr/src/app/UI
# Copy configuration files
COPY UI/package*.json ./
# Install project dependencies
# RUN npm ci
RUN npm install
# Copy project files
COPY UI/ .
# Build the project
RUN npm run build

# Production stage
FROM nginx:alpine AS production
# Copy build files
COPY --from=builder /usr/src/app/UI/dist /usr/share/nginx/html
# Configuración para manejar rutas de Astro con i18n
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Start Nginx
CMD ["nginx", "-g", "daemon off;"]