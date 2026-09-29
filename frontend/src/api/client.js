import axios from 'axios'

const API_URL = (import.meta.env.VITE_API_URL || 'https://raudev-h.pro').replace(/\/+$/, '')

const client = axios.create({
  baseURL: API_URL,
})

// Endpoints that don't require auth: login/register and public reads of the catalog
function isPublic(config) {
  const url = config.url || ''
  const method = (config.method || 'get').toLowerCase()
  if (url.startsWith('/auth/login') || url.startsWith('/auth/register')) return true
  return method === 'get' && (url.startsWith('/product') || url.startsWith('/category'))
}

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token && !isPublic(config)) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default client
