import axios from 'axios'

// All API files import this instead of axios directly.
// Change the baseURL here and every request across the app updates automatically.
// In Docker, nginx proxies /api/ to the backend — set VITE_API_URL=/api at build time.
// For local dev, defaults to http://localhost:8000.
export default axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})
