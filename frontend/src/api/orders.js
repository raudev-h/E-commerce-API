import client from './client'

export async function getOrders() {
  const response = await client.get('/order')
  return response.data
}

export async function getOrder(id) {
  const response = await client.get(`/order/${id}`)
  return response.data
}

export async function createOrder(data) {
  const response = await client.post('/order', data)
  return response.data
}

export async function cancelOrder(id) {
  const response = await client.patch(`/order/${id}`)
  return response.data
}
