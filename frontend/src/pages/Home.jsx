import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] px-6 text-center">
      <h1 className="font-display text-5xl font-bold text-white mb-4">
        Welcome to <span className="text-brand">ShopAPI</span>
      </h1>
      <p className="text-white/50 text-lg mb-8 max-w-md">
        Browse our catalog, add items to your cart, and track your orders.
      </p>
      <Link
        to="/products"
        className="px-6 py-3 bg-brand text-base font-semibold rounded-lg hover:bg-brand/90 transition-colors"
      >
        Browse Products
      </Link>
    </div>
  )
}
