import client from './client'

export async function login(email, password) {
  const form = new URLSearchParams()
  form.append('username', email)  // OAuth2PasswordRequestForm field name is always 'username'
  form.append('password', password)
  const response = await client.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export async function register(userData) {
  const response = await client.post('/user/', userData)
  return response.data
}

export async function getMe() {
  const response = await client.get('/auth/me')
  return response.data
}
