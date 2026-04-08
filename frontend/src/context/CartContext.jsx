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
    const updated = await updateCartItem(itemId, quantity)
    setCart(updated)
    return updated
  }

  async function removeItem(itemId) {
    const updated = await removeCartItem(itemId)
    setCart(updated)
    return updated
  }

  async function emptyCart() {
    const updated = await clearCartApi()
    setCart(updated)
    return updated
  }

  return (
    <CartContext.Provider value={{ cart, loading, itemCount, addItem, updateItem, removeItem, emptyCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  return useContext(CartContext)
}
