import client from './client'

export async function getUsers() {
  const response = await client.get('/user')
  return response.data
}

export async function updateUser(id, data) {
  const response = await client.patch(`/user/${id}`, data)
  return response.data
}
