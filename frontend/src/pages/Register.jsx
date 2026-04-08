import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register as registerRequest } from '../api/auth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: '',
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  function handleChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await registerRequest(form)
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] px-6">
      <div className="w-full max-w-sm">
        <h1 className="font-display text-3xl font-bold text-white mb-8 text-center">
          Register
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="grid grid-cols-2 gap-3">
            <Input
              label="First name"
              type="text"
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              required
              placeholder="John"
            />
            <Input
              label="Last name"
              type="text"
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              required
              placeholder="Doe"
            />
          </div>
          <Input
            label="Email"
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
            placeholder="you@example.com"
          />
          <Input
            label="Password"
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
            placeholder="••••••••"
          />
          <Input
            label="Confirm password"
            type="password"
            name="confirm_password"
            value={form.confirm_password}
            onChange={handleChange}
            required
            placeholder="••••••••"
          />

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <Button type="submit" loading={loading} className="mt-2 py-2.5">
            {loading ? 'Creating account…' : 'Create account'}
          </Button>
        </form>

        <p className="text-center text-white/40 text-sm mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-brand hover:underline">
            Login
          </Link>
        </p>
      </div>
    </div>
  )
}
