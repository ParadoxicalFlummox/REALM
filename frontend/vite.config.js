import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  // Read .env from the repo root instead of frontend/ — single .env for the whole project.
  envDir: '../',
})
