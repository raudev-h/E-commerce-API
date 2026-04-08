import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login as loginRequest } from '../api/auth'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const data = await loginRequest(username, password)
      login(data.access_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] px-6">
      <div className="w-full max-w-sm">
        <h1 className="font-display text-3xl font-bold text-white mb-8 text-center">
          Login
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-sm text-white/60">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="bg-surface border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-white/30 focus:outline-none focus:border-brand transition-colors"
              placeholder="your_username"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm text-white/60">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="bg-surface border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-white/30 focus:outline-none focus:border-brand transition-colors"
              placeholder="••••••••"
            />
          </div>

          {error && (
            <p className="text-red-400 text-sm">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-2 py-2.5 bg-brand text-base font-semibold rounded-lg hover:bg-brand/90 transition-colors disabled:opacity-50"
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="text-center text-white/40 text-sm mt-6">
          Don&apos;t have an account?{' '}
          <Link to="/register" className="text-brand hover:underline">
            Register
          </Link>
        </p>
      </div>
    </div>
  )
}
