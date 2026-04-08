import client from './client'

export async function getOrders() {
  const response = await client.get('/orders')
  return response.data
}

export async function getOrder(id) {
  const response = await client.get(`/orders/${id}`)
  return response.data
}

export async function createOrder(data) {
  const response = await client.post('/orders', data)
  return response.data
}

export async function cancelOrder(id) {
  const response = await client.patch(`/orders/${id}/cancel`)
  return response.data
}
