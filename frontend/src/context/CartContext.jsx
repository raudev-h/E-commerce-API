import { createContext, useContext, useState, useEffect } from 'react'
import { useAuth } from './AuthContext'
import {
  getCart,
  addToCart,
  updateCartItem,
  removeCartItem,
  clearCart as clearCartApi,
} from '../api/cart'

const CartContext = createContext(null)

export function CartProvider({ children }) {
  const { user } = useAuth()
  const [cart, setCart] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!user) {
      setCart(null)
      return
    }
    setLoading(true)
    getCart()
      .then(setCart)
      .catch(() => setCart(null))
      .finally(() => setLoading(false))
  }, [user])

  const itemCount = cart?.items?.reduce((sum, item) => sum + item.quantity, 0) ?? 0

  async function addItem(productId, quantity = 1) {
    await addToCart(productId, quantity)
    const updated = await getCart()
    setCart(updated)
  }

  async function updateItem(itemId, quantity) {
    await updateCartItem(itemId, quantity)
    const updated = await getCart()
    setCart(updated)
    return updated
  }

  async function removeItem(itemId) {
    await removeCartItem(itemId)
    const updated = await getCart()
    setCart(updated)
    return updated
  }

  async function emptyCart() {
    await clearCartApi()
    const updated = await getCart()
    setCart(updated)
    return updated
  }

  async function refreshCart() {
    try {
      const updated = await getCart()
      setCart(updated)
    } catch {
      setCart(null)
    }
  }

  return (
    <CartContext.Provider value={{ cart, loading, itemCount, addItem, updateItem, removeItem, emptyCart, refreshCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  return useContext(CartContext)
}
