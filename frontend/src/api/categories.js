import client from './client'

export async function getCategories() {
  const response = await client.get('/categories')
  return response.data
}

export async function getCategory(id) {
  const response = await client.get(`/categories/${id}`)
  return response.data
}

export async function createCategory(data) {
  const response = await client.post('/categories', data)
  return response.data
}

export async function updateCategory(id, data) {
  const response = await client.put(`/categories/${id}`, data)
  return response.data
}

export async function deleteCategory(id) {
  const response = await client.delete(`/categories/${id}`)
  return response.data
}
