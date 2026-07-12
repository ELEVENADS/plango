import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  root: path.resolve(__dirname, 'src/render'),
  base: './',
  build: {
    outDir: path.resolve(__dirname, 'dist/render'),
    emptyOutDir: true,
  },
  server: {
    port: 5173,
  },
})
