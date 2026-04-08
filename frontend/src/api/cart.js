import client from './client'

export async function getCart() {
  const response = await client.get('/cart')
  return response.data
}

export async function addToCart(productId, quantity) {
  const response = await client.post('/cart/items', { product_id: productId, quantity })
  return response.data
}

export async function updateCartItem(itemId, quantity) {
  const response = await client.put(`/cart/items/${itemId}`, { quantity })
  return response.data
}

export async function removeCartItem(itemId) {
  const response = await client.delete(`/cart/items/${itemId}`)
  return response.data
}

export async function clearCart() {
  const response = await client.delete('/cart')
  return response.data
}
