import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Cart, CartItem } from '@/types'
import { cartApi } from '@/services/api'

export const useCartStore = defineStore('cart', () => {
  const cart = ref<Cart | null>(null)
  const loading = ref(false)

  const items = computed(() => cart.value?.items || [])
  const itemsCount = computed(() => cart.value?.items_count || 0)
  const subtotal = computed(() => cart.value?.subtotal || 0)
  const discount = computed(() => cart.value?.discount || 0)
  const deliveryFee = computed(() => cart.value?.delivery_fee || 0)
  const total = computed(() => cart.value?.total || 0)

  async function fetchCart() {
    loading.value = true
    try {
      cart.value = await cartApi.getCart()
    } catch (error) {
      console.error('Failed to fetch cart:', error)
    } finally {
      loading.value = false
    }
  }

  async function addItem(productId: number, quantity = 1, size?: string, color?: string) {
    loading.value = true
    try {
      cart.value = await cartApi.addItem(productId, quantity, size, color)
    } finally {
      loading.value = false
    }
  }

  async function updateItem(itemId: number, quantity: number) {
    loading.value = true
    try {
      cart.value = await cartApi.updateItem(itemId, quantity)
    } finally {
      loading.value = false
    }
  }

  async function removeItem(itemId: number) {
    loading.value = true
    try {
      cart.value = await cartApi.removeItem(itemId)
    } finally {
      loading.value = false
    }
  }

  // Initialize cart
  fetchCart()

  return {
    cart,
    loading,
    items,
    itemsCount,
    subtotal,
    discount,
    deliveryFee,
    total,
    fetchCart,
    addItem,
    updateItem,
    removeItem,
  }
})
