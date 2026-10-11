import { useState, useEffect, useRef } from 'react'
import { getSalesReport, getTopProducts, getLowStock } from '../../api/reports'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

const DEFAULT_RANGE_DAYS = 30
const TOP_PRODUCTS_LIMIT = 10
const DEFAULT_LOW_STOCK_THRESHOLD = 5
const RELOAD_DELAY_MS = 400

function toDateInput(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function defaultRange() {
  const end = new Date()
  const start = new Date()
  start.setDate(end.getDate() - DEFAULT_RANGE_DAYS)
  return { startDate: toDateInput(start), endDate: toDateInput(end) }
}

function formatMoney(value) {
  return Number(value).toLocaleString('en-US', { style: 'currency', currency: 'USD' })
}

function formatPeriod(iso, granularity) {
  const options =
    granularity === 'month'
      ? { year: 'numeric', month: 'short' }
      : { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(iso).toLocaleDateString('en-US', options)
}

function errorMessage(err, fallback) {
  const detail = err.response?.data?.detail
  return typeof detail === 'string' ? detail : fallback
}

function Section({ title, aside, children }) {
  return (
    <section className="mb-10">
      <div className="flex items-end justify-between gap-4 mb-4">
        <h2 className="font-display text-lg font-bold text-white">{title}</h2>
        {aside}
      </div>
      {children}
    </section>
  )
}

function ReportTable({ headers, loading, empty, children }) {
  if (loading) return <p className="text-white/40">Loading…</p>
  if (empty) return <p className="text-white/40">{empty}</p>
  if (!children?.length) return null

  return (
    <div className="border border-white/10 rounded-xl overflow-hidden">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-white/10 text-white/40 text-left">
            {headers.map((header) => (
              <th key={header} className="px-4 py-3 font-medium">{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
    </div>
  )
}

export default function AdminReports() {
  const [range, setRange] = useState(defaultRange)
  const [granularity, setGranularity] = useState('day')
  const [sales, setSales] = useState(null)
  const [topProducts, setTopProducts] = useState([])
  const [salesLoading, setSalesLoading] = useState(true)
  const [salesError, setSalesError] = useState(null)

  const [threshold, setThreshold] = useState(DEFAULT_LOW_STOCK_THRESHOLD)
  const [lowStock, setLowStock] = useState([])
  const [lowStockLoading, setLowStockLoading] = useState(true)
  const [lowStockError, setLowStockError] = useState(null)

  const latestSalesRequest = useRef(0)

  async function loadSales() {
    const requestId = ++latestSalesRequest.current
    setSalesLoading(true)
    setSalesError(null)
    try {
      const [salesData, topData] = await Promise.all([
        getSalesReport({ ...range, granularity }),
        getTopProducts({ ...range, limit: TOP_PRODUCTS_LIMIT }),
      ])
      if (requestId !== latestSalesRequest.current) return // a newer filter change is already loading
      setSales(salesData)
      setTopProducts(topData.rows)
    } catch (err) {
      if (requestId !== latestSalesRequest.current) return
      setSales(null)
      setTopProducts([])
      setSalesError(errorMessage(err, 'Could not load sales reports'))
    } finally {
      if (requestId === latestSalesRequest.current) setSalesLoading(false)
    }
  }

  async function loadLowStock() {
    setLowStockLoading(true)
    setLowStockError(null)
    try {
      const data = await getLowStock(threshold)
      setLowStock(data.rows)
    } catch (err) {
      setLowStock([])
      setLowStockError(errorMessage(err, 'Could not load low stock report'))
    } finally {
      setLowStockLoading(false)
    }
  }

  // Reload sales and top products whenever the dates or granularity change
  useEffect(() => {
    if (!range.startDate || !range.endDate) return
    if (range.startDate > range.endDate) {
      latestSalesRequest.current++ // discard any response still in flight
      setSales(null)
      setTopProducts([])
      setSalesLoading(false)
      setSalesError('Start date must be on or before the end date')
      return
    }
    const timer = setTimeout(loadSales, RELOAD_DELAY_MS)
    return () => clearTimeout(timer)
  }, [range, granularity])

  useEffect(() => { loadLowStock() }, [])

  function handleRangeChange(e) {
    setRange((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  function handleGranularityChange(e) {
    setGranularity(e.target.value)
  }

  function handleThresholdSubmit(e) {
    e.preventDefault()
    loadLowStock()
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Reports</h1>
      </div>

      <div className="flex flex-wrap items-end gap-3 mb-8">
        <Input
          label="Start date"
          name="startDate"
          type="date"
          required
          value={range.startDate}
          max={range.endDate}
          onChange={handleRangeChange}
          className="[color-scheme:dark]"
        />
        <Input
          label="End date"
          name="endDate"
          type="date"
          required
          value={range.endDate}
          min={range.startDate}
          onChange={handleRangeChange}
          className="[color-scheme:dark]"
        />
      </div>

      {salesError && <p className="text-red-400 text-sm mb-8">{salesError}</p>}

      <Section
        title="Sales"
        aside={
          <select
            value={granularity}
            onChange={handleGranularityChange}
            aria-label="Granularity"
            className="bg-surface border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-brand/50"
          >
            <option value="day">By day</option>
            <option value="month">By month</option>
          </select>
        }
      >
        {sales && (
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="border border-white/10 rounded-xl px-4 py-3">
              <p className="text-xs text-white/40 mb-1">Total orders</p>
              <p className="font-display text-2xl font-bold text-white">{sales.total_orders}</p>
            </div>
            <div className="border border-white/10 rounded-xl px-4 py-3">
              <p className="text-xs text-white/40 mb-1">Total revenue</p>
              <p className="font-display text-2xl font-bold text-brand">{formatMoney(sales.grand_total)}</p>
            </div>
          </div>
        )}
        <ReportTable
          headers={['Period', 'Orders', 'Revenue', 'Average ticket']}
          loading={salesLoading}
          empty={!salesError && !sales?.rows.length && 'No sales in this period.'}
        >
          {sales?.rows.map((row) => (
            <tr key={row.period} className="border-b border-white/5 hover:bg-white/[0.02]">
              <td className="px-4 py-3 text-white font-medium">{formatPeriod(row.period, sales.granularity)}</td>
              <td className="px-4 py-3 text-white/50">{row.orders_count}</td>
              <td className="px-4 py-3 text-white/50">{formatMoney(row.total_revenue)}</td>
              <td className="px-4 py-3 text-white/50">{formatMoney(row.average_ticket)}</td>
            </tr>
          ))}
        </ReportTable>
      </Section>

      <Section title="Top products">
        <ReportTable
          headers={['Product', 'Units sold', 'Revenue']}
          loading={salesLoading}
          empty={!salesError && !topProducts.length && 'No products sold in this period.'}
        >
          {topProducts.map((row) => (
            <tr key={row.product_id} className="border-b border-white/5 hover:bg-white/[0.02]">
              <td className="px-4 py-3 text-white font-medium">{row.product_name}</td>
              <td className="px-4 py-3 text-white/50">{row.units_sold}</td>
              <td className="px-4 py-3 text-white/50">{formatMoney(row.revenue)}</td>
            </tr>
          ))}
        </ReportTable>
      </Section>

      <Section
        title="Low stock"
        aside={
          <form onSubmit={handleThresholdSubmit} className="flex items-center gap-2">
            <label htmlFor="threshold" className="text-sm text-white/40">Stock at or below</label>
            <input
              id="threshold"
              type="number"
              min="0"
              required
              value={threshold}
              onChange={(e) => setThreshold(e.target.value)}
              className="w-20 bg-surface border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-brand/50"
            />
            <Button type="submit" variant="secondary" loading={lowStockLoading} className="px-3 py-1.5 text-sm">
              Update
            </Button>
          </form>
        }
      >
        {lowStockError && <p className="text-red-400 text-sm mb-4">{lowStockError}</p>}
        <ReportTable
          headers={['Product', 'Category', 'Stock']}
          loading={lowStockLoading}
          empty={!lowStock.length && 'No products at or below this stock level.'}
        >
          {lowStock.map((row) => (
            <tr key={row.product_id} className="border-b border-white/5 hover:bg-white/[0.02]">
              <td className="px-4 py-3 text-white font-medium">{row.product_name}</td>
              <td className="px-4 py-3 text-white/50">{row.category_name ?? '—'}</td>
              <td className="px-4 py-3">
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  row.stock === 0 ? 'bg-red-500/10 text-red-400' : 'bg-yellow-500/10 text-yellow-400'
                }`}>
                  {row.stock}
                </span>
              </td>
            </tr>
          ))}
        </ReportTable>
      </Section>
    </div>
  )
}
