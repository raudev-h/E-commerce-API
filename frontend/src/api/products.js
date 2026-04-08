import client from './client'

export async function getProducts(params) {
  const response = await client.get('/products', { params })
  return response.data
}

export async function getProduct(id) {
  const response = await client.get(`/products/${id}`)
  return response.data
}

export async function createProduct(data) {
  const response = await client.post('/products', data)
  return response.data
}

export async function updateProduct(id, data) {
  const response = await client.put(`/products/${id}`, data)
  return response.data
}

export async function deleteProduct(id) {
  const response = await client.delete(`/products/${id}`)
  return response.data
}
