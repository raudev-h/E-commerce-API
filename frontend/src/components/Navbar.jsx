import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-surface border-b border-white/10">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link
          to="/"
          className="font-display text-xl font-bold tracking-tight text-brand"
        >
          ShopAPI
        </Link>

        <div className="flex items-center gap-6">
          <Link
            to="/"
            className="text-sm text-white/70 hover:text-white transition-colors"
          >
            Home
          </Link>
          <Link
            to="/products"
            className="text-sm text-white/70 hover:text-white transition-colors"
          >
            Products
          </Link>
          <Link
            to="/cart"
            className="text-sm text-white/70 hover:text-white transition-colors"
          >
            Cart
          </Link>
        </div>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <span className="text-sm text-white/50">
                {user.sub || user.email || user.username}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm px-4 py-1.5 rounded-md border border-white/20 text-white/70 hover:text-white hover:border-white/40 transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-sm text-white/70 hover:text-white transition-colors"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="text-sm px-4 py-1.5 rounded-md bg-brand text-base font-medium hover:bg-brand/90 transition-colors"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
