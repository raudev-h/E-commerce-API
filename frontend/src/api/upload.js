import client from './client'

export async function uploadImage(file) {
  const form = new FormData()
  form.append('file', file)
  const response = await client.post('/upload/image', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data.url
}
