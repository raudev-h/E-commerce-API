import client from './client'

export async function getCategories() {
  const response = await client.get('/category')
  return response.data
}

export async function getCategory(id) {
  const response = await client.get(`/category/${id}`)
  return response.data
}

export async function createCategory(data) {
  const response = await client.post('/category', data)
  return response.data
}

export async function updateCategory(id, data) {
  const response = await client.patch(`/category/${id}`, data)
  return response.data
}

export async function deleteCategory(id) {
  const response = await client.delete(`/category/${id}`)
  return response.data
}
