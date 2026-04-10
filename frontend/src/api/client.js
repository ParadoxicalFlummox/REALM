import axios from 'axios'

// All API files import this instead of axios directly.
// Change the baseURL here and every request across the app updates automatically.
export default axios.create({
  baseURL: 'http://localhost:8000',
})
