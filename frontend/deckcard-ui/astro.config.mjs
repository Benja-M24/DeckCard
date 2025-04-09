// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
    output: 'static',
    vite: {
        server: {
            allowedHosts: ['deckcards.lussocastelli.com'],
            proxy: {
                '/api': {
                    target: 'http://backend:8800',
                    changeOrigin: true,
                    secure: false,
                    rewrite: (path) => path.replace(/^\/api/, ''),
                    configure: (proxy, _options) => {
                        proxy.on('error', (err, _req, _res) => {
                            console.log('proxy error', err);
                        });
                        proxy.on('proxyReq', (proxyReq, req, _res) => {
                            console.log('Sending Request:', req.method, req.url);
                        });
                        proxy.on('proxyRes', (proxyRes, req, _res) => {
                            console.log('Received Response from:', req.method, req.url, proxyRes.statusCode);
                        });
                    }
                }
            }
        },
        // Optimizaciones para producción
        build: {
            minify: true,
            cssMinify: true,
            rollupOptions: {
                output: {
                    manualChunks: {
                        'react-vendor': ['react', 'react-dom'],
                    },
                },
            },
        }
    },
    // Configuración de integraciones
    integrations: [
        // Integración de Tailwind CSS
        tailwind(),
        // Integración de React para componentes interactivos
        react({
            // Modo de renderizado: client-only para archivos .tsx/.jsx
            include: ['**/*.tsx', '**/*.jsx'],
        })
    ],
    // El output: 'static' genera archivos HTML estáticos durante el build
    // No necesitamos adapter cuando usamos static output
    
    // Deshabilitar la barra de herramientas de desarrollo
    devToolbar: {
        enabled: false
    }
});


