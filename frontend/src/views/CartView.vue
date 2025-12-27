<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()
const promoCode = ref('')
const applyingPromo = ref(false)

async function updateQuantity(itemId: number, quantity: number) {
  await cartStore.updateItem(itemId, quantity)
}

async function removeItem(itemId: number) {
  if (confirm('Are you sure you want to remove this item?')) {
    await cartStore.removeItem(itemId)
  }
}

function applyPromoCode() {
  if (promoCode.value.trim()) {
    applyingPromo.value = true
    setTimeout(() => {
      alert('Promo code applied: ' + promoCode.value)
      applyingPromo.value = false
    }, 500)
  }
}
</script>

<template>
  <div class="py-8">
    <div class="container-custom">
      <!-- Breadcrumbs -->
      <nav class="flex items-center gap-2 text-sm mb-8">
        <RouterLink to="/" class="text-gray-500 hover:text-black">Home</RouterLink>
        <span class="text-gray-400">/</span>
        <span class="font-medium">Cart</span>
      </nav>

      <h1 class="heading-lg mb-8">YOUR CART</h1>

      <!-- Loading -->
      <div v-if="cartStore.loading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
      </div>

      <!-- Empty Cart -->
      <div v-else-if="cartStore.items.length === 0" class="text-center py-20">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto text-gray-300 mb-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p class="text-gray-500 text-lg mb-6">Your cart is empty</p>
        <RouterLink to="/shop" class="btn-primary inline-block">
          Continue Shopping
        </RouterLink>
      </div>

      <!-- Cart Content -->
      <div v-else class="grid lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2 border border-gray-200 rounded-2xl p-6">
          <div class="space-y-6">
            <div
              v-for="item in cartStore.items"
              :key="item.id"
              class="flex gap-4 pb-6 border-b border-gray-200 last:border-0 last:pb-0"
            >
              <!-- Product Image -->
              <div class="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                <img
                  :src="item.product_image || 'https://via.placeholder.com/200'"
                  :alt="item.product_name"
                  class="w-full h-full object-cover"
                />
              </div>

              <!-- Product Details -->
              <div class="flex-1">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-medium">{{ item.product_name }}</h3>
                    <p class="text-sm text-gray-500 mt-1">
                      Size: {{ item.size }}
                      <span v-if="item.color"> | Color: {{ item.color }}</span>
                    </p>
                  </div>
                  <button
                    @click="removeItem(item.id)"
                    class="text-red-500 hover:text-red-600"
                    aria-label="Remove item"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>

                <div class="flex items-center justify-between mt-4">
                  <span class="font-bold text-lg">${{ item.discount_price || item.price }}</span>
                  <div class="flex items-center border border-gray-300 rounded-full">
                    <button
                      @click="updateQuantity(item.id, item.quantity - 1)"
                      class="w-8 h-8 flex items-center justify-center hover:bg-gray-100 rounded-l-full"
                    >
                      -
                    </button>
                    <span class="w-8 text-center text-sm">{{ item.quantity }}</span>
                    <button
                      @click="updateQuantity(item.id, item.quantity + 1)"
                      class="w-8 h-8 flex items-center justify-center hover:bg-gray-100 rounded-r-full"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="border border-gray-200 rounded-2xl p-6 h-fit">
          <h2 class="font-bold text-xl mb-6">Order Summary</h2>

          <div class="space-y-4 mb-6">
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal</span>
              <span class="font-medium">${{ cartStore.subtotal.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Discount (-20%)</span>
              <span class="font-medium text-red-500">-${{ cartStore.discount.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Delivery Fee</span>
              <span class="font-medium">${{ cartStore.deliveryFee.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between pt-4 border-t border-gray-200">
              <span class="font-bold">Total</span>
              <span class="font-bold text-xl">${{ cartStore.total.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Promo Code -->
          <div class="flex gap-3 mb-6">
            <div class="relative flex-1">
              <input
                v-model="promoCode"
                type="text"
                placeholder="Add promo code"
                class="w-full bg-gray-100 rounded-full py-3 pl-12 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
            <button
              @click="applyPromoCode"
              :disabled="applyingPromo"
              class="bg-black text-white px-6 py-3 rounded-full font-medium hover:bg-gray-800 disabled:opacity-50"
            >
              Apply
            </button>
          </div>

          <!-- Checkout Button -->
          <button class="btn-primary w-full flex items-center justify-center gap-2">
            Go to Checkout
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
