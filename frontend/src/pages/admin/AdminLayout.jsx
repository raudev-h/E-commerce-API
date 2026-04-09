import { NavLink, Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function AdminLayout() {
  const { user } = useAuth()

  if (!user || user.role !== 'admin') {
    return <Navigate to="/" replace />
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 flex gap-8">
      <aside className="w-48 shrink-0">
        <p className="text-xs font-semibold uppercase tracking-widest text-white/30 mb-4">
          Admin
        </p>
        <nav className="flex flex-col gap-1">
          <NavLink
            to="/admin/products"
            className={({ isActive }) =>
              `px-3 py-2 rounded-md text-sm transition-colors ${
                isActive
                  ? 'bg-brand/10 text-brand font-medium'
                  : 'text-white/60 hover:text-white hover:bg-white/5'
              }`
            }
          >
            Products
          </NavLink>
          <NavLink
            to="/admin/categories"
            className={({ isActive }) =>
              `px-3 py-2 rounded-md text-sm transition-colors ${
                isActive
                  ? 'bg-brand/10 text-brand font-medium'
                  : 'text-white/60 hover:text-white hover:bg-white/5'
              }`
            }
          >
            Categories
          </NavLink>
        </nav>
      </aside>

      <div className="flex-1 min-w-0">
        <Outlet />
      </div>
    </div>
  )
}
