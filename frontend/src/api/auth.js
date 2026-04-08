import client from './client'

export async function login(username, password) {
  const form = new URLSearchParams()
  form.append('username', username)
  form.append('password', password)
  const response = await client.post('/auth/token', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export async function register(userData) {
  const response = await client.post('/auth/register', userData)
  return response.data
}

export async function getMe() {
  const response = await client.get('/auth/me')
  return response.data
}
