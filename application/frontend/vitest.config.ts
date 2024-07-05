import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true, 
    environment: 'jsdom', 
  },
  define: {
    'VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'http://localhost:5656')
  }
})