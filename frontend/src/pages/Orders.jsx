import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getOrders, cancelOrder } from '../api/orders'

const STATUS_CONFIG = {
  pending:    { label: 'Pending',    color: 'text-amber-400',  bg: 'bg-amber-400/10',  border: 'border-amber-400/20' },
  confirmed:  { label: 'Confirmed',  color: 'text-blue-400',   bg: 'bg-blue-400/10',   border: 'border-blue-400/20' },
  shipped:    { label: 'Shipped',    color: 'text-purple-400', bg: 'bg-purple-400/10', border: 'border-purple-400/20' },
  delivered:  { label: 'Delivered',  color: 'text-brand',      bg: 'bg-brand/10',      border: 'border-brand/20' },
  cancelled:  { label: 'Cancelled',  color: 'text-white/30',   bg: 'bg-white/5',       border: 'border-white/10' },
}

function StatusBadge({ status }) {
  const cfg = STATUS_CONFIG[status] ?? STATUS_CONFIG.pending
  return (
    <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full border ${cfg.color} ${cfg.bg} ${cfg.border} tracking-wide`}>
      {cfg.label}
    </span>
  )
}

function SkeletonOrder() {
  return (
    <div className="bg-surface border border-white/5 rounded-2xl p-5 animate-pulse flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="h-4 bg-white/5 rounded-full w-28" />
        <div className="h-6 bg-white/5 rounded-full w-20" />
      </div>
      <div className="h-3 bg-white/5 rounded-full w-40" />
      <div className="border-t border-white/5 pt-4 flex flex-col gap-2">
        <div className="h-3 bg-white/5 rounded-full w-full" />
        <div className="h-3 bg-white/5 rounded-full w-3/4" />
      </div>
    </div>
  )
}

function OrderCard({ order, onCancel }) {
  const [expanded, setExpanded] = useState(false)
  const [cancelling, setCancelling] = useState(false)

  const canCancel = order.status === 'pending'
  const items = order.items ?? []
  const total = items.reduce(
    (sum, item) => sum + Number(item.unit_price ?? item.product?.price ?? 0) * item.quantity,
    0
  )

  async function handleCancel() {
    setCancelling(true)
    try {
      await onCancel(order.id)
    } finally {
      setCancelling(false)
    }
  }

  function formatDate(iso) {
    if (!iso) return ''
    return new Date(iso).toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit',
    })
  }

  return (
    <div className="bg-surface border border-white/5 rounded-2xl overflow-hidden transition-all duration-200">

      {/* Header */}
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full text-left p-5 flex items-start sm:items-center justify-between gap-4 hover:bg-white/[0.02] transition-colors"
      >
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-3">
            <span className="font-display font-semibold text-white text-sm">
              Order #{order.id}
            </span>
            <StatusBadge status={order.status} />
          </div>
          <span className="text-xs text-white/25">{formatDate(order.created_at)}</span>
        </div>

        <div className="flex items-center gap-4 shrink-0">
          <span className="font-display font-bold text-brand tabular-nums">
            ${total.toFixed(2)}
          </span>
          <svg
            className={`w-4 h-4 text-white/25 transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Expanded items */}
      {expanded && (
        <div className="border-t border-white/[0.06] px-5 pb-5 pt-4 flex flex-col gap-3">

          {items.length === 0 ? (
            <p className="text-white/25 text-sm">No item details available.</p>
          ) : (
            items.map((item, i) => (
              <div key={item.id ?? i} className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-white/[0.04] border border-white/5 overflow-hidden shrink-0">
                  {item.product?.image_url ? (
                    <img src={item.product.image_url} alt={item.product.name} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white/10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                          d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10" />
                      </svg>
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-white/80 truncate">
                    {item.product?.name ?? `Item #${item.product_id}`}
                  </p>
                  <p className="text-xs text-white/25 tabular-nums">
                    {item.quantity} × ${Number(item.unit_price ?? item.product?.price ?? 0).toFixed(2)}
                  </p>
                </div>
                <span className="text-sm font-semibold text-white/60 tabular-nums shrink-0">
                  ${(Number(item.unit_price ?? item.product?.price ?? 0) * item.quantity).toFixed(2)}
                </span>
              </div>
            ))
          )}

          {canCancel && (
            <div className="pt-3 border-t border-white/[0.06]">
              <button
                onClick={handleCancel}
                disabled={cancelling}
                className="text-xs text-red-400/60 hover:text-red-400 transition-colors disabled:opacity-40"
              >
                {cancelling ? 'Cancelling…' : 'Cancel order'}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getOrders()
      .then((data) => setOrders(Array.isArray(data) ? data : []))
      .catch(() => setError('Could not load your orders.'))
      .finally(() => setLoading(false))
  }, [])

  async function handleCancel(orderId) {
    const updated = await cancelOrder(orderId)
    setOrders((prev) => prev.map((o) => (o.id === orderId ? { ...o, ...updated } : o)))
  }

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-12 flex flex-col gap-4">
        <div className="h-8 bg-white/5 rounded-full w-24 mb-6 animate-pulse" />
        {Array.from({ length: 3 }).map((_, i) => <SkeletonOrder key={i} />)}
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] gap-3">
        <p className="text-white/30 text-sm">{error}</p>
        <button onClick={() => window.location.reload()} className="text-xs text-brand/50 hover:text-brand transition-colors">
          Retry
        </button>
      </div>
    )
  }

  if (orders.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] gap-5">
        <div className="w-20 h-20 rounded-2xl bg-surface border border-white/5 flex items-center justify-center">
          <svg className="w-8 h-8 text-white/10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <div className="text-center">
          <p className="font-display text-xl font-semibold text-white/20 mb-1">No orders yet</p>
          <p className="text-white/20 text-sm">Your order history will appear here.</p>
        </div>
        <Link
          to="/products"
          className="mt-2 px-5 py-2.5 bg-brand text-[#0a0a0a] text-sm font-semibold rounded-xl hover:bg-brand/90 transition-colors"
        >
          Start shopping
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <div className="mb-10">
        <h1 className="font-display text-4xl font-bold text-white tracking-tight">Orders</h1>
        <p className="text-white/30 text-sm mt-1.5">
          {orders.length} order{orders.length !== 1 ? 's' : ''}
        </p>
      </div>

      <div className="flex flex-col gap-3">
        {orders.map((order) => (
          <OrderCard key={order.id} order={order} onCancel={handleCancel} />
        ))}
      </div>
    </div>
  )
}
