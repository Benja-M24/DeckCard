// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
    output: 'server',
    vite: {
        plugins: [tailwindcss()],
        server: {
            allowedHosts: ['deckcards.lussocastelli.com'],
            proxy: {
                '/api': {
                    target: 'http://backend:8800',
                    changeOrigin: true,
                    secure: false
                }
            }
        }
    },
});
