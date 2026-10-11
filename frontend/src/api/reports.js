import client from './client'

export async function getSalesReport({ startDate, endDate, granularity }) {
  const response = await client.get('/reports/sales', {
    params: { start_date: startDate, end_date: endDate, granularity },
  })
  return response.data
}

export async function getTopProducts({ startDate, endDate, limit }) {
  const response = await client.get('/reports/top-products', {
    params: { start_date: startDate, end_date: endDate, limit },
  })
  return response.data
}

export async function getLowStock(threshold) {
  const response = await client.get('/reports/low-stock', { params: { threshold } })
  return response.data
}
