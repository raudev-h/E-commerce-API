import { useState, useEffect } from 'react'
import { getUsers, updateUser } from '../../api/users'
import { useAuth } from '../../context/AuthContext'

export default function AdminUsers() {
  const { user: currentUser } = useAuth()
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [updating, setUpdating] = useState(null) // id being updated

  async function load() {
    setLoading(true)
    try {
      const data = await getUsers()
      setUsers(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function toggleActive(user) {
    setUpdating(user.id)
    try {
      const updated = await updateUser(user.id, { is_active: !user.is_active })
      setUsers((prev) => prev.map((u) => (u.id === user.id ? updated : u)))
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not update user')
    } finally {
      setUpdating(null)
    }
  }

  async function toggleRole(user) {
    const newRole = user.role === 'admin' ? 'user' : 'admin'
    setUpdating(user.id)
    try {
      const updated = await updateUser(user.id, { role: newRole })
      setUsers((prev) => prev.map((u) => (u.id === user.id ? updated : u)))
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not update user')
    } finally {
      setUpdating(null)
    }
  }

  function formatDate(iso) {
    return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Users</h1>
        <span className="text-sm text-white/30">{users.length} total</span>
      </div>

      {loading ? (
        <p className="text-white/40">Loading…</p>
      ) : (
        <div className="border border-white/10 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 text-white/40 text-left">
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Email</th>
                <th className="px-4 py-3 font-medium">Created</th>
                <th className="px-4 py-3 font-medium">Updated</th>
                <th className="px-4 py-3 font-medium w-32"></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => {
                const isCurrentUser = u.id === currentUser?.sub
                const busy = updating === u.id
                return (
                  <tr key={u.id} className="border-b border-white/5 hover:bg-white/[0.02]">
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        u.is_active
                          ? 'bg-green-500/10 text-green-400'
                          : 'bg-white/5 text-white/30'
                      }`}>
                        {u.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-white font-medium">
                      {u.first_name} {u.last_name}
                    </td>
                    <td className="px-4 py-3 text-white/50">{u.email}</td>
                    <td className="px-4 py-3 text-white/30 text-xs">{formatDate(u.created_at)}</td>
                    <td className="px-4 py-3 text-white/30 text-xs">{formatDate(u.updated_at)}</td>
                    <td className="px-4 py-3">
                      {!isCurrentUser && (
                        <div className="flex gap-3 justify-end">
                          <button
                            onClick={() => toggleRole(u)}
                            disabled={busy}
                            className="text-xs text-white/40 hover:text-white transition-colors disabled:opacity-30"
                          >
                            {busy ? '…' : u.role === 'admin' ? 'Make user' : 'Make admin'}
                          </button>
                          <button
                            onClick={() => toggleActive(u)}
                            disabled={busy}
                            className={`text-xs transition-colors disabled:opacity-30 ${
                              u.is_active
                                ? 'text-red-400/60 hover:text-red-400'
                                : 'text-green-400/60 hover:text-green-400'
                            }`}
                          >
                            {busy ? '…' : u.is_active ? 'Deactivate' : 'Activate'}
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
