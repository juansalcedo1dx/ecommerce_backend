import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'   // ← IMPORTANTE

// Configuración del proxy al backend Django
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // ← ACTIVA el alias "@/"
    },
  },
  server: {
    host: 'localhost',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: '../staticfiles/frontend',
    emptyOutDir: true,
  },
})
