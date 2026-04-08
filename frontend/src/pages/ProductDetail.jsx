import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getProduct } from '../api/products'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'

export default function ProductDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const { addItem } = useCart()
  const navigate = useNavigate()

  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [quantity, setQuantity] = useState(1)
  const [adding, setAdding] = useState(false)
  const [added, setAdded] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getProduct(id)
      .then(setProduct)
      .catch(() => setError('Product not found.'))
      .finally(() => setLoading(false))
  }, [id])

  async function handleAddToCart() {
    if (!user) {
      navigate('/login')
      return
    }
    if (adding) return
    setAdding(true)
    try {
      await addItem(product.id, quantity)
      setAdded(true)
      setTimeout(() => setAdded(false), 2500)
    } finally {
      setAdding(false)
    }
  }

  function changeQty(delta) {
    setQuantity((q) => {
      const next = q + delta
      const max = product?.stock ?? 99
      return Math.min(Math.max(1, next), max)
    })
  }

  // --- Loading skeleton ---
  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-12 animate-pulse">
        <div className="h-4 bg-white/5 rounded-full w-32 mb-10" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div className="aspect-square bg-surface rounded-2xl" />
          <div className="flex flex-col gap-4 py-2">
            <div className="h-3 bg-white/5 rounded-full w-20" />
            <div className="h-8 bg-white/5 rounded-full w-3/4" />
            <div className="h-3 bg-white/5 rounded-full w-full mt-2" />
            <div className="h-3 bg-white/5 rounded-full w-5/6" />
            <div className="h-3 bg-white/5 rounded-full w-4/6" />
            <div className="h-10 bg-white/5 rounded-xl w-28 mt-4" />
            <div className="h-12 bg-white/5 rounded-xl w-full mt-2" />
          </div>
        </div>
      </div>
    )
  }

  // --- Error ---
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] gap-4">
        <p className="text-white/30 font-display text-xl">{error}</p>
        <Link to="/products" className="text-sm text-brand/60 hover:text-brand transition-colors">
          ← Back to products
        </Link>
      </div>
    )
  }

  const outOfStock = product.stock === 0
  const lowStock = product.stock > 0 && product.stock <= 5

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">

      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-white/30 mb-10">
        <Link to="/products" className="hover:text-white/60 transition-colors">
          Products
        </Link>
        <span>/</span>
        {product.category && (
          <>
            <span className="text-white/30">{product.category.name}</span>
            <span>/</span>
          </>
        )}
        <span className="text-white/60 truncate max-w-xs">{product.name}</span>
      </nav>

      {/* Main layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 lg:gap-16">

        {/* Image */}
        <div className="aspect-square bg-surface rounded-2xl border border-white/5 overflow-hidden relative">
          {product.image_url ? (
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <svg className="w-16 h-16 text-white/8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10" />
              </svg>
            </div>
          )}

          {outOfStock && (
            <div className="absolute inset-0 bg-black/70 flex items-center justify-center backdrop-blur-[1px]">
              <span className="text-xs font-semibold text-white/40 tracking-[0.2em] uppercase">
                Out of stock
              </span>
            </div>
          )}
        </div>

        {/* Info */}
        <div className="flex flex-col">

          {/* Category + badges */}
          <div className="flex items-center gap-3 mb-3">
            {product.category && (
              <span className="text-[11px] font-semibold text-brand/60 tracking-[0.15em] uppercase">
                {product.category.name}
              </span>
            )}
            {lowStock && (
              <span className="text-[10px] font-semibold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-2 py-0.5 rounded-full">
                Only {product.stock} left
              </span>
            )}
          </div>

          {/* Name */}
          <h1 className="font-display text-3xl lg:text-4xl font-bold text-white leading-tight mb-4">
            {product.name}
          </h1>

          {/* Price */}
          <div className="mb-6">
            <span className="font-display text-4xl font-bold text-brand tabular-nums">
              ${Number(product.price).toFixed(2)}
            </span>
          </div>

          {/* Description */}
          {product.description && (
            <p className="text-white/45 leading-relaxed text-[15px] mb-8">
              {product.description}
            </p>
          )}

          {/* Divider */}
          <div className="border-t border-white/[0.06] mb-8" />

          {/* Quantity + Add to cart */}
          {!outOfStock ? (
            <div className="flex items-center gap-4">

              {/* Qty selector */}
              <div className="flex items-center gap-1 bg-surface border border-white/10 rounded-xl overflow-hidden">
                <button
                  onClick={() => changeQty(-1)}
                  disabled={quantity <= 1}
                  className="w-10 h-10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors disabled:opacity-25 disabled:cursor-not-allowed"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M20 12H4" />
                  </svg>
                </button>
                <span className="w-10 text-center font-display font-semibold text-white text-sm tabular-nums">
                  {quantity}
                </span>
                <button
                  onClick={() => changeQty(1)}
                  disabled={quantity >= (product.stock ?? 99)}
                  className="w-10 h-10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors disabled:opacity-25 disabled:cursor-not-allowed"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
                  </svg>
                </button>
              </div>

              {/* Add to cart button */}
              <button
                onClick={handleAddToCart}
                disabled={adding}
                className={`flex-1 h-10 rounded-xl font-semibold text-sm transition-all duration-200 flex items-center justify-center gap-2
                  ${added
                    ? 'bg-brand/20 text-brand border border-brand/30'
                    : 'bg-brand text-[#0a0a0a] hover:bg-brand/90 active:scale-[0.98]'
                  } disabled:opacity-60`}
              >
                {adding ? (
                  <>
                    <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                    Adding…
                  </>
                ) : added ? (
                  <>
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                    </svg>
                    Added to cart
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                        d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    Add to cart
                  </>
                )}
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3 py-3 px-4 bg-white/[0.03] border border-white/8 rounded-xl">
              <span className="text-white/30 text-sm">This product is currently unavailable.</span>
            </div>
          )}

          {/* Stock info */}
          {!outOfStock && product.stock !== undefined && (
            <p className="text-xs text-white/20 mt-4">
              {product.stock} unit{product.stock !== 1 ? 's' : ''} in stock
            </p>
          )}

          {/* View cart shortcut — shown after adding */}
          {added && (
            <Link
              to="/cart"
              className="mt-3 text-sm text-brand/60 hover:text-brand transition-colors self-start"
            >
              View cart →
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}
