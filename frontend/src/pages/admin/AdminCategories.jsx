import { useState, useEffect } from 'react'
import { getCategories, createCategory, updateCategory, deleteCategory } from '../../api/categories'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

const EMPTY_FORM = { name: '', description: '' }

export default function AdminCategories() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [modal, setModal] = useState(null) // null | { mode: 'create' | 'edit', data?: category }
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [deleteId, setDeleteId] = useState(null)

  async function load() {
    setLoading(true)
    try {
      const data = await getCategories()
      setCategories(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function openCreate() {
    setForm(EMPTY_FORM)
    setError(null)
    setModal({ mode: 'create' })
  }

  function openEdit(category) {
    setForm({ name: category.name, description: category.description || '' })
    setError(null)
    setModal({ mode: 'edit', data: category })
  }

  function handleChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      const payload = {
        name: form.name,
        description: form.description || undefined,
      }
      if (modal.mode === 'create') {
        await createCategory(payload)
      } else {
        await updateCategory(modal.data.id, payload)
      }
      setModal(null)
      await load()
    } catch (err) {
      const detail = err.response?.data?.detail
      setError(Array.isArray(detail) ? detail.map((e) => e.msg).join(', ') : detail || 'Something went wrong')
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete(id) {
    setDeleteId(id)
    try {
      await deleteCategory(id)
      await load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not delete category')
    } finally {
      setDeleteId(null)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Categories</h1>
        <Button onClick={openCreate} className="px-4 py-2 text-sm">
          + New category
        </Button>
      </div>

      {loading ? (
        <p className="text-white/40">Loading…</p>
      ) : categories.length === 0 ? (
        <p className="text-white/40">No categories yet.</p>
      ) : (
        <div className="border border-white/10 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 text-white/40 text-left">
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Description</th>
                <th className="px-4 py-3 font-medium">Active</th>
                <th className="px-4 py-3 font-medium w-28"></th>
              </tr>
            </thead>
            <tbody>
              {categories.map((cat) => (
                <tr key={cat.id} className="border-b border-white/5 hover:bg-white/[0.02]">
                  <td className="px-4 py-3 text-white font-medium">{cat.name}</td>
                  <td className="px-4 py-3 text-white/50">{cat.description || '—'}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${cat.is_active ? 'bg-green-500/10 text-green-400' : 'bg-white/5 text-white/30'}`}>
                      {cat.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2 justify-end">
                      <button
                        onClick={() => openEdit(cat)}
                        className="text-xs text-white/50 hover:text-white transition-colors"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(cat.id)}
                        disabled={deleteId === cat.id}
                        className="text-xs text-red-400/60 hover:text-red-400 transition-colors disabled:opacity-50"
                      >
                        {deleteId === cat.id ? '…' : 'Delete'}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {modal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="bg-surface border border-white/10 rounded-xl p-6 w-full max-w-md">
            <h2 className="font-display text-lg font-bold text-white mb-5">
              {modal.mode === 'create' ? 'New category' : 'Edit category'}
            </h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <Input
                label="Name"
                name="name"
                value={form.name}
                onChange={handleChange}
                required
                placeholder="Electronics"
              />
              <Input
                label="Description (optional)"
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="All electronic devices"
              />
              {error && <p className="text-red-400 text-sm">{error}</p>}
              <div className="flex gap-3 justify-end mt-2">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setModal(null)}
                  className="px-4 py-2 text-sm"
                >
                  Cancel
                </Button>
                <Button type="submit" loading={saving} className="px-4 py-2 text-sm">
                  {modal.mode === 'create' ? 'Create' : 'Save'}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
