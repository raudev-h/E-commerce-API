import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const { itemCount } = useCart()
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)

  function handleLogout() {
    logout()
    setOpen(false)
    navigate('/login')
  }

  function close() {
    setOpen(false)
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-surface border-b border-white/10">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">

        {/* Logo */}
        <Link to="/" onClick={close} className="font-display text-xl font-bold tracking-tight text-brand">
          ShopAPI
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-6">
          <Link to="/" className="text-sm text-white/70 hover:text-white transition-colors">Home</Link>
          <Link to="/products" className="text-sm text-white/70 hover:text-white transition-colors">Products</Link>
          <Link to="/cart" className="relative text-sm text-white/70 hover:text-white transition-colors">
            Cart
            {itemCount > 0 && (
              <span className="absolute -top-2 -right-3.5 min-w-[16px] h-4 bg-brand text-[#0a0a0a] text-[10px] font-bold rounded-full flex items-center justify-center px-1 tabular-nums">
                {itemCount > 99 ? '99+' : itemCount}
              </span>
            )}
          </Link>
          {user?.role === 'admin' && (
            <Link to="/admin" className="text-sm text-brand/80 hover:text-brand transition-colors font-medium">Admin</Link>
          )}
        </div>

        {/* Desktop auth */}
        <div className="hidden md:flex items-center gap-4">
          {user ? (
            <>
              <span className="text-sm text-white/50">{user.sub || user.email}</span>
              <button
                onClick={handleLogout}
                className="text-sm px-4 py-1.5 rounded-md border border-white/20 text-white/70 hover:text-white hover:border-white/40 transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm text-white/70 hover:text-white transition-colors">Login</Link>
              <Link to="/register" className="text-sm px-4 py-1.5 rounded-md bg-brand text-base font-medium hover:bg-brand/90 transition-colors">
                Register
              </Link>
            </>
          )}
        </div>

        {/* Mobile right side: cart badge + hamburger */}
        <div className="flex md:hidden items-center gap-4">
          <Link to="/cart" onClick={close} className="relative text-sm text-white/70 hover:text-white transition-colors">
            Cart
            {itemCount > 0 && (
              <span className="absolute -top-2 -right-3.5 min-w-[16px] h-4 bg-brand text-[#0a0a0a] text-[10px] font-bold rounded-full flex items-center justify-center px-1 tabular-nums">
                {itemCount > 99 ? '99+' : itemCount}
              </span>
            )}
          </Link>

          <button
            onClick={() => setOpen((o) => !o)}
            className="text-white/60 hover:text-white transition-colors p-1"
            aria-label="Toggle menu"
          >
            {open ? (
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden border-t border-white/10 bg-surface px-6 py-4 flex flex-col gap-4">
          <Link to="/" onClick={close} className="text-sm text-white/70 hover:text-white transition-colors py-1">Home</Link>
          <Link to="/products" onClick={close} className="text-sm text-white/70 hover:text-white transition-colors py-1">Products</Link>
          <Link to="/orders" onClick={close} className="text-sm text-white/70 hover:text-white transition-colors py-1">Orders</Link>
          {user?.role === 'admin' && (
            <Link to="/admin" onClick={close} className="text-sm text-brand/80 hover:text-brand transition-colors font-medium py-1">Admin</Link>
          )}

          <div className="border-t border-white/10 pt-4">
            {user ? (
              <div className="flex flex-col gap-3">
                <span className="text-sm text-white/40">{user.sub || user.email}</span>
                <button
                  onClick={handleLogout}
                  className="text-sm text-left text-white/70 hover:text-white transition-colors"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex flex-col gap-3">
                <Link to="/login" onClick={close} className="text-sm text-white/70 hover:text-white transition-colors">Login</Link>
                <Link to="/register" onClick={close} className="text-sm text-brand hover:text-brand/80 transition-colors font-medium">Register</Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}
