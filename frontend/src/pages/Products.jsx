import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getProducts } from '../api/products'
import { getCategories } from '../api/categories'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'

function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(t)
  }, [value, delay])
  return debounced
}

function SkeletonCard() {
  return (
    <div className="bg-surface rounded-2xl overflow-hidden border border-white/5 animate-pulse">
      <div className="aspect-[4/3] bg-white/5" />
      <div className="p-5 flex flex-col gap-3">
        <div className="h-3 bg-white/5 rounded-full w-1/4" />
        <div className="h-5 bg-white/5 rounded-full w-3/4" />
        <div className="h-3 bg-white/5 rounded-full w-full" />
        <div className="h-3 bg-white/5 rounded-full w-2/3" />
        <div className="flex items-center justify-between mt-2 pt-4 border-t border-white/5">
          <div className="h-6 bg-white/5 rounded-full w-16" />
          <div className="h-7 bg-white/5 rounded-lg w-20" />
        </div>
      </div>
    </div>
  )
}

function ProductCard({ product, onAddToCart }) {
  const [adding, setAdding] = useState(false)
  const [added, setAdded] = useState(false)

  async function handleAdd(e) {
    e.preventDefault()
    e.stopPropagation()
    if (adding || product.stock === 0) return
    setAdding(true)
    try {
      await onAddToCart(product.id)
      setAdded(true)
      setTimeout(() => setAdded(false), 2200)
    } catch {
      // onAddToCart handles errors externally
    } finally {
      setAdding(false)
    }
  }

  const outOfStock = product.stock === 0
  const lowStock = product.stock !== undefined && product.stock > 0 && product.stock <= 5

  return (
    <Link
      to={`/products/${product.id}`}
      className="group bg-surface rounded-2xl overflow-hidden border border-white/5 hover:border-brand/25 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-black/40 flex flex-col"
    >
      {/* Image */}
      <div className="aspect-[4/3] bg-gradient-to-br from-white/5 to-white/[0.02] relative overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-[1.04] transition-transform duration-500 ease-out"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <svg
              className="w-10 h-10 text-white/10"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1}
                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10"
              />
            </svg>
          </div>
        )}

        {outOfStock && (
          <div className="absolute inset-0 bg-black/70 flex items-center justify-center backdrop-blur-[1px]">
            <span className="text-[10px] font-semibold text-white/40 tracking-[0.2em] uppercase">
              Out of stock
            </span>
          </div>
        )}

        {lowStock && (
          <div className="absolute top-3 right-3">
            <span className="text-[10px] font-semibold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-2 py-1 rounded-full tracking-wide">
              {product.stock} left
            </span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-5 flex flex-col gap-2.5 flex-1">
        {product.category && (
          <span className="text-[11px] font-semibold text-brand/60 tracking-[0.15em] uppercase">
            {product.category.name}
          </span>
        )}

        <h3 className="font-display font-semibold text-white text-[15px] leading-snug group-hover:text-brand/90 transition-colors duration-200 line-clamp-2">
          {product.name}
        </h3>

        {product.description && (
          <p className="text-white/35 text-sm leading-relaxed line-clamp-2 flex-1">
            {product.description}
          </p>
        )}

        <div className="flex items-center justify-between mt-auto pt-4 border-t border-white/[0.06]">
          <span className="font-display text-xl font-bold text-brand tabular-nums">
            ${Number(product.price).toFixed(2)}
          </span>

          <button
            onClick={handleAdd}
            disabled={adding || outOfStock}
            className={`
              text-xs px-3.5 py-1.5 rounded-lg font-medium border transition-all duration-200
              ${added
                ? 'bg-brand/15 text-brand border-brand/30 scale-95'
                : outOfStock
                  ? 'text-white/20 border-white/5 cursor-not-allowed'
                  : 'text-white/50 border-white/10 hover:bg-brand hover:text-[#0a0a0a] hover:border-brand hover:scale-105 active:scale-95'
              }
              disabled:opacity-50
            `}
          >
            {adding ? (
              <span className="inline-flex items-center gap-1.5">
                <span className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
              </span>
            ) : added ? (
              '✓ Added'
            ) : (
              '+ Cart'
            )}
          </button>
        </div>
      </div>
    </Link>
  )
}

function EmptyState({ hasFilters, onClear }) {
  return (
    <div className="col-span-full flex flex-col items-center justify-center py-28 gap-4">
      <div className="w-16 h-16 rounded-2xl bg-white/[0.03] border border-white/5 flex items-center justify-center mb-2">
        <svg className="w-7 h-7 text-white/15" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <p className="font-display text-xl font-semibold text-white/20">
        {hasFilters ? 'No results found' : 'No products yet'}
      </p>
      {hasFilters && (
        <button
          onClick={onClear}
          className="text-sm text-brand/50 hover:text-brand transition-colors"
        >
          Clear filters
        </button>
      )}
    </div>
  )
}

export default function Products() {
  const { user } = useAuth()
  const { addItem } = useCart()
  const navigate = useNavigate()

  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [toast, setToast] = useState(null)

  const debouncedSearch = useDebounce(search, 380)

  useEffect(() => {
    getCategories()
      .then(setCategories)
      .catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    setError(null)
    const params = {}
    if (debouncedSearch) params.search = debouncedSearch
    if (selectedCategory) params.category_id = selectedCategory
    getProducts(params)
      .then(setProducts)
      .catch(() => setError('Could not load products. Please try again.'))
      .finally(() => setLoading(false))
  }, [debouncedSearch, selectedCategory])

  async function handleAddToCart(productId) {
    if (!user) {
      navigate('/login')
      return
    }
    await addItem(productId, 1)
    setToast('Added to cart')
    setTimeout(() => setToast(null), 2500)
  }

  function clearFilters() {
    setSearch('')
    setSelectedCategory(null)
  }

  const hasFilters = !!search || !!selectedCategory

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">

      {/* Header */}
      <div className="mb-10">
        <h1 className="font-display text-4xl font-bold text-white tracking-tight">
          Products
        </h1>
        <p className="text-white/30 text-sm mt-1.5">
          {loading
            ? 'Loading…'
            : `${products.length} item${products.length !== 1 ? 's' : ''}${hasFilters ? ' found' : ''}`
          }
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-8">

        {/* Search */}
        <div className="relative">
          <svg
            className="absolute left-3.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/25 pointer-events-none"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search products…"
            className="w-full sm:w-64 bg-surface border border-white/8 rounded-xl pl-9 pr-9 py-2.5 text-white text-sm placeholder-white/25 focus:outline-none focus:border-brand/40 transition-colors"
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-white/25 hover:text-white/60 transition-colors"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* Category pills */}
        {categories.length > 0 && (
          <div className="flex items-center gap-2 overflow-x-auto pb-0.5 scrollbar-none flex-1">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`shrink-0 text-xs px-3.5 py-1.5 rounded-full border font-medium transition-all duration-150 ${
                !selectedCategory
                  ? 'bg-brand text-[#0a0a0a] border-brand'
                  : 'border-white/10 text-white/40 hover:text-white/70 hover:border-white/20'
              }`}
            >
              All
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(selectedCategory === cat.id ? null : cat.id)}
                className={`shrink-0 text-xs px-3.5 py-1.5 rounded-full border font-medium transition-all duration-150 ${
                  selectedCategory === cat.id
                    ? 'bg-brand text-[#0a0a0a] border-brand'
                    : 'border-white/10 text-white/40 hover:text-white/70 hover:border-white/20'
                }`}
              >
                {cat.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="flex flex-col items-center py-24 gap-3">
          <p className="text-red-400/80 text-sm">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="text-xs text-white/30 hover:text-white/60 transition-colors"
          >
            Retry
          </button>
        </div>
      )}

      {/* Grid */}
      {!error && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {loading
            ? Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)
            : products.length === 0
              ? <EmptyState hasFilters={hasFilters} onClear={clearFilters} />
              : products.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    onAddToCart={handleAddToCart}
                  />
                ))
          }
        </div>
      )}

      {/* Toast notification */}
      <div
        className={`fixed bottom-8 left-1/2 -translate-x-1/2 z-50 transition-all duration-300 ${
          toast ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2 pointer-events-none'
        }`}
      >
        <div className="flex items-center gap-2.5 bg-[#111] border border-brand/20 text-white text-sm px-5 py-3 rounded-full shadow-2xl shadow-black/50">
          <span className="w-4 h-4 rounded-full bg-brand/20 flex items-center justify-center shrink-0">
            <svg className="w-2.5 h-2.5 text-brand" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          </span>
          {toast}
        </div>
      </div>
    </div>
  )
}
