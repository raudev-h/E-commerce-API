import client from './client'

export async function getProducts(params) {
  const response = await client.get('/product', { params })
  return response.data
}

export async function getProduct(id) {
  const response = await client.get(`/product/${id}`)
  return response.data
}

export async function createProduct(data) {
  const response = await client.post('/product', data)
  return response.data
}

export async function updateProduct(id, data) {
  const response = await client.patch(`/product/${id}`, data)
  return response.data
}

export async function deleteProduct(id) {
  const response = await client.delete(`/product/${id}`)
  return response.data
}
