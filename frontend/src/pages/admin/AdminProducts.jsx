import { useState, useEffect, useRef } from 'react'
import { getProducts, createProduct, updateProduct, deleteProduct } from '../../api/products'
import { getCategories } from '../../api/categories'
import { uploadImage } from '../../api/upload'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

const EMPTY_FORM = {
  name: '',
  description: '',
  price: '',
  stock: '',
  category_id: '',
  image_url: '',
}

export default function AdminProducts() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [modal, setModal] = useState(null) // null | { mode: 'create' | 'edit', data?: product }
  const [form, setForm] = useState(EMPTY_FORM)
  const [imagePreview, setImagePreview] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [deleteId, setDeleteId] = useState(null)
  const fileRef = useRef(null)

  async function load() {
    setLoading(true)
    try {
      const [prods, cats] = await Promise.all([
        getProducts({ limit: 100 }),
        getCategories(),
      ])
      setProducts(prods)
      setCategories(cats)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function openCreate() {
    setForm(EMPTY_FORM)
    setImagePreview(null)
    setError(null)
    setModal({ mode: 'create' })
  }

  function openEdit(product) {
    setForm({
      name: product.name,
      description: product.description || '',
      price: String(product.price),
      stock: String(product.stock),
      category_id: product.category_id,
      image_url: product.image_url || '',
    })
    setImagePreview(product.image_url || null)
    setError(null)
    setModal({ mode: 'edit', data: product })
  }

  function handleChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleFileChange(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    setError(null)
    try {
      const url = await uploadImage(file)
      setForm((prev) => ({ ...prev, image_url: url }))
      setImagePreview(url)
    } catch (err) {
      setError('Image upload failed: ' + (err.response?.data?.detail || err.message))
    } finally {
      setUploading(false)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      const payload = {
        name: form.name,
        description: form.description || undefined,
        price: parseFloat(form.price),
        stock: parseInt(form.stock, 10),
        category_id: form.category_id,
        image_url: form.image_url || undefined,
      }
      if (modal.mode === 'create') {
        await createProduct(payload)
      } else {
        await updateProduct(modal.data.id, payload)
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
      await deleteProduct(id)
      await load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not delete product')
    } finally {
      setDeleteId(null)
    }
  }

  function categoryName(id) {
    return categories.find((c) => c.id === id)?.name ?? '—'
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Products</h1>
        <Button onClick={openCreate} className="px-4 py-2 text-sm">
          + New product
        </Button>
      </div>

      {loading ? (
        <p className="text-white/40">Loading…</p>
      ) : products.length === 0 ? (
        <p className="text-white/40">No products yet.</p>
      ) : (
        <div className="border border-white/10 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 text-white/40 text-left">
                <th className="px-4 py-3 font-medium">Image</th>
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Category</th>
                <th className="px-4 py-3 font-medium">Price</th>
                <th className="px-4 py-3 font-medium">Stock</th>
                <th className="px-4 py-3 font-medium">Active</th>
                <th className="px-4 py-3 font-medium w-28"></th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id} className="border-b border-white/5 hover:bg-white/[0.02]">
                  <td className="px-4 py-3">
                    {p.image_url ? (
                      <img src={p.image_url} alt={p.name} className="w-10 h-10 object-cover rounded-md" />
                    ) : (
                      <div className="w-10 h-10 rounded-md bg-white/5 flex items-center justify-center text-white/20 text-xs">
                        No img
                      </div>
                    )}
                  </td>
                  <td className="px-4 py-3 text-white font-medium">{p.name}</td>
                  <td className="px-4 py-3 text-white/50">{categoryName(p.category_id)}</td>
                  <td className="px-4 py-3 text-white">${p.price.toFixed(2)}</td>
                  <td className="px-4 py-3 text-white/70">{p.stock}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${p.is_active ? 'bg-green-500/10 text-green-400' : 'bg-white/5 text-white/30'}`}>
                      {p.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2 justify-end">
                      <button
                        onClick={() => openEdit(p)}
                        className="text-xs text-white/50 hover:text-white transition-colors"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(p.id)}
                        disabled={deleteId === p.id}
                        className="text-xs text-red-400/60 hover:text-red-400 transition-colors disabled:opacity-50"
                      >
                        {deleteId === p.id ? '…' : 'Delete'}
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
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4 overflow-y-auto py-8">
          <div className="bg-surface border border-white/10 rounded-xl p-6 w-full max-w-lg my-auto">
            <h2 className="font-display text-lg font-bold text-white mb-5">
              {modal.mode === 'create' ? 'New product' : 'Edit product'}
            </h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              {/* Image upload */}
              <div>
                <label className="block text-sm text-white/60 mb-2">Image</label>
                <div className="flex items-center gap-4">
                  {imagePreview ? (
                    <img src={imagePreview} alt="preview" className="w-16 h-16 object-cover rounded-lg border border-white/10" />
                  ) : (
                    <div className="w-16 h-16 rounded-lg border border-dashed border-white/20 flex items-center justify-center text-white/20 text-xs">
                      No img
                    </div>
                  )}
                  <div className="flex flex-col gap-1">
                    <button
                      type="button"
                      onClick={() => fileRef.current?.click()}
                      disabled={uploading}
                      className="text-sm text-brand hover:text-brand/80 transition-colors disabled:opacity-50"
                    >
                      {uploading ? 'Uploading…' : 'Upload image'}
                    </button>
                    {imagePreview && (
                      <button
                        type="button"
                        onClick={() => { setImagePreview(null); setForm((p) => ({ ...p, image_url: '' })) }}
                        className="text-xs text-white/30 hover:text-white/60 transition-colors"
                      >
                        Remove
                      </button>
                    )}
                  </div>
                </div>
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </div>

              <Input
                label="Name"
                name="name"
                value={form.name}
                onChange={handleChange}
                required
                placeholder="Wireless headphones"
              />
              <Input
                label="Description (optional)"
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="At least 10 characters"
              />
              <div className="grid grid-cols-2 gap-3">
                <Input
                  label="Price"
                  name="price"
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.price}
                  onChange={handleChange}
                  required
                  placeholder="29.99"
                />
                <Input
                  label="Stock"
                  name="stock"
                  type="number"
                  min="0"
                  step="1"
                  value={form.stock}
                  onChange={handleChange}
                  required
                  placeholder="100"
                />
              </div>

              <div>
                <label className="block text-sm text-white/60 mb-1.5">Category</label>
                <select
                  name="category_id"
                  value={form.category_id}
                  onChange={handleChange}
                  required
                  className="w-full bg-white/5 border border-white/10 text-white rounded-md px-3 py-2 text-sm focus:outline-none focus:border-brand/60"
                >
                  <option value="" disabled>Select a category</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                  ))}
                </select>
              </div>

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
                <Button type="submit" loading={saving} disabled={uploading} className="px-4 py-2 text-sm">
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
