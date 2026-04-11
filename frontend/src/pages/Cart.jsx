import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { createOrder } from '../api/orders'
import { useCart } from '../context/CartContext'

function SkeletonRow() {
  return (
    <div className="flex items-center gap-5 py-5 border-b border-white/[0.06] animate-pulse">
      <div className="w-16 h-16 rounded-xl bg-white/5 shrink-0" />
      <div className="flex-1 flex flex-col gap-2">
        <div className="h-4 bg-white/5 rounded-full w-1/2" />
        <div className="h-3 bg-white/5 rounded-full w-1/4" />
      </div>
      <div className="h-4 bg-white/5 rounded-full w-16" />
    </div>
  )
}

function CartItem({ item, onUpdateQty, onRemove }) {
  const [qty, setQty] = useState(item.quantity)
  const [updating, setUpdating] = useState(false)
  const [removing, setRemoving] = useState(false)

  // Keep local qty in sync when context updates the item
  useEffect(() => { setQty(item.quantity) }, [item.quantity])

  async function handleQty(delta) {
    const next = qty + delta
    if (next < 1) return
    setQty(next)
    setUpdating(true)
    try {
      await onUpdateQty(item.id, next)
    } catch {
      setQty(qty) // revert on error
    } finally {
      setUpdating(false)
    }
  }

  async function handleRemove() {
    setRemoving(true)
    try {
      await onRemove(item.id)
    } finally {
      setRemoving(false)
    }
  }

  const product = item.product
  const lineTotal = Number(product?.price ?? 0) * qty

  return (
    <div className={`flex items-center gap-4 sm:gap-5 py-5 border-b border-white/[0.06] transition-opacity duration-200 ${removing ? 'opacity-30 pointer-events-none' : ''}`}>

      {/* Thumbnail */}
      <Link to={`/products/${product?.id}`} className="shrink-0">
        <div className="w-16 h-16 rounded-xl bg-surface border border-white/5 overflow-hidden">
          {product?.image_url ? (
            <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <svg className="w-6 h-6 text-white/10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10" />
              </svg>
            </div>
          )}
        </div>
      </Link>

      {/* Name + category */}
      <div className="flex-1 min-w-0">
        <Link to={`/products/${product?.id}`} className="hover:text-brand transition-colors">
          <p className="font-display font-semibold text-white text-sm leading-snug truncate">
            {product?.name ?? 'Product'}
          </p>
        </Link>
        {product?.category && (
          <p className="text-[11px] text-white/30 mt-0.5 tracking-wide">{product.category.name}</p>
        )}
        <p className="text-xs text-white/20 mt-1 tabular-nums">
          ${Number(product?.price ?? 0).toFixed(2)} each
        </p>
      </div>

      {/* Qty controls */}
      <div className="flex items-center gap-1 bg-surface border border-white/8 rounded-lg overflow-hidden shrink-0">
        <button
          onClick={() => handleQty(-1)}
          disabled={qty <= 1 || updating}
          className="w-8 h-8 flex items-center justify-center text-white/30 hover:text-white hover:bg-white/5 transition-colors disabled:opacity-20 disabled:cursor-not-allowed"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M20 12H4" />
          </svg>
        </button>
        <span className={`w-7 text-center text-sm font-semibold text-white tabular-nums transition-opacity ${updating ? 'opacity-40' : ''}`}>
          {qty}
        </span>
        <button
          onClick={() => handleQty(1)}
          disabled={updating}
          className="w-8 h-8 flex items-center justify-center text-white/30 hover:text-white hover:bg-white/5 transition-colors disabled:opacity-20 disabled:cursor-not-allowed"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>

      {/* Line total */}
      <span className="font-display font-bold text-white text-sm tabular-nums w-16 text-right shrink-0">
        ${lineTotal.toFixed(2)}
      </span>

      {/* Remove */}
      <button
        onClick={handleRemove}
        disabled={removing}
        className="text-white/20 hover:text-red-400 transition-colors shrink-0 ml-1"
        aria-label="Remove item"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  )
}

export default function Cart() {
  const navigate = useNavigate()
  const { cart, loading, updateItem, removeItem, emptyCart, refreshCart } = useCart()

  const [placingOrder, setPlacingOrder] = useState(false)
  const [orderError, setOrderError] = useState(null)

  const error = !loading && cart === null ? 'Could not load your cart.' : null

  async function handleUpdateQty(itemId, quantity) {
    await updateItem(itemId, quantity)
  }

  async function handleRemove(itemId) {
    await removeItem(itemId)
  }

  async function handleClear() {
    await emptyCart()
  }

  async function handlePlaceOrder() {
    setPlacingOrder(true)
    setOrderError(null)
    try {
      await createOrder({})
      await refreshCart()
      navigate('/orders')
    } catch (err) {
      const detail = err.response?.data?.detail
      setOrderError(Array.isArray(detail) ? detail.map((e) => e.msg).join(', ') : detail || 'Could not place the order. Please try again.')
    } finally {
      setPlacingOrder(false)
    }
  }

  const items = cart?.items ?? []
  const total = items.reduce(
    (sum, item) => sum + Number(item.product?.price ?? 0) * item.quantity,
    0
  )
  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0)

  // --- Loading ---
  if (loading) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-12">
        <div className="h-8 bg-white/5 rounded-full w-24 mb-10 animate-pulse" />
        {Array.from({ length: 3 }).map((_, i) => <SkeletonRow key={i} />)}
      </div>
    )
  }

  // --- Error ---
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

  // --- Empty ---
  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] gap-5">
        <div className="w-20 h-20 rounded-2xl bg-surface border border-white/5 flex items-center justify-center">
          <svg className="w-8 h-8 text-white/10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
              d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div className="text-center">
          <p className="font-display text-xl font-semibold text-white/20 mb-1">Your cart is empty</p>
          <p className="text-white/20 text-sm">Add some products to get started.</p>
        </div>
        <Link
          to="/products"
          className="mt-2 px-5 py-2.5 bg-brand text-[#0a0a0a] text-sm font-semibold rounded-xl hover:bg-brand/90 transition-colors"
        >
          Browse products
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">

      {/* Header */}
      <div className="flex items-center justify-between mb-10">
        <div>
          <h1 className="font-display text-4xl font-bold text-white tracking-tight">Cart</h1>
          <p className="text-white/30 text-sm mt-1.5">
            {itemCount} item{itemCount !== 1 ? 's' : ''}
          </p>
        </div>
        <button
          onClick={handleClear}
          className="text-xs text-white/25 hover:text-red-400 transition-colors"
        >
          Clear all
        </button>
      </div>

      {/* Items */}
      <div>
        {items.map((item) => (
          <CartItem
            key={item.id}
            item={item}
            onUpdateQty={handleUpdateQty}
            onRemove={handleRemove}
          />
        ))}
      </div>

      {/* Summary */}
      <div className="mt-8 bg-surface border border-white/[0.06] rounded-2xl p-6 flex flex-col gap-4">

        <div className="flex items-center justify-between text-white/40 text-sm">
          <span>Subtotal ({itemCount} item{itemCount !== 1 ? 's' : ''})</span>
          <span className="tabular-nums">${total.toFixed(2)}</span>
        </div>

        <div className="border-t border-white/[0.06]" />

        <div className="flex items-center justify-between">
          <span className="font-display font-bold text-white text-lg">Total</span>
          <span className="font-display font-bold text-brand text-2xl tabular-nums">
            ${total.toFixed(2)}
          </span>
        </div>

        {orderError && (
          <p className="text-red-400/80 text-xs">{orderError}</p>
        )}

        <button
          onClick={handlePlaceOrder}
          disabled={placingOrder}
          className="w-full h-12 bg-brand text-[#0a0a0a] font-semibold rounded-xl hover:bg-brand/90 active:scale-[0.98] transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed mt-1"
        >
          {placingOrder ? (
            <>
              <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
              Placing order…
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M5 13l4 4L19 7" />
              </svg>
              Place order
            </>
          )}
        </button>

        <Link
          to="/products"
          className="text-center text-xs text-white/25 hover:text-white/50 transition-colors"
        >
          ← Continue shopping
        </Link>
      </div>
    </div>
  )
}
