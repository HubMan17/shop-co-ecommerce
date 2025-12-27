<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const searchQuery = ref('')
const isMobileMenuOpen = ref(false)

const cartItemsCount = computed(() => cartStore.itemsCount)

const navLinks = [
  { name: 'Shop', path: '/shop' },
  { name: 'On Sale', path: '/shop?sort=discount' },
  { name: 'New Arrivals', path: '/shop?filter=new' },
  { name: 'Brands', path: '/shop' },
]

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/shop', query: { search: searchQuery.value } })
    searchQuery.value = ''
  }
}
</script>

<template>
  <header class="bg-white border-b border-gray-100 sticky top-0 z-50">
    <div class="container-custom">
      <div class="flex items-center justify-between h-16 lg:h-20">
        <!-- Mobile Menu Button -->
        <button 
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          class="lg:hidden p-2"
          aria-label="Toggle menu"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Logo -->
        <RouterLink to="/" class="text-2xl lg:text-3xl font-bold" style="font-family: 'Integral CF', sans-serif;">
          SHOP.CO
        </RouterLink>

        <!-- Desktop Navigation -->
        <nav class="hidden lg:flex items-center space-x-8">
          <RouterLink 
            v-for="link in navLinks" 
            :key="link.path"
            :to="link.path"
            class="text-gray-700 hover:text-black transition-colors"
          >
            {{ link.name }}
          </RouterLink>
        </nav>

        <!-- Search Bar (Desktop) -->
        <div class="hidden lg:flex flex-1 max-w-md mx-8">
          <form @submit.prevent="handleSearch" class="w-full relative">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search for products..."
              class="w-full bg-gray-100 rounded-full py-3 pl-12 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            />
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </form>
        </div>

        <!-- Right Icons -->
        <div class="flex items-center space-x-4">
          <!-- Search (Mobile) -->
          <button class="lg:hidden p-2" aria-label="Search">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>

          <!-- Cart -->
          <RouterLink to="/cart" class="relative p-2" aria-label="Cart">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span 
              v-if="cartItemsCount > 0"
              class="absolute -top-1 -right-1 bg-black text-white text-xs w-5 h-5 rounded-full flex items-center justify-center"
            >
              {{ cartItemsCount }}
            </span>
          </RouterLink>

          <!-- User -->
          <RouterLink 
            :to="authStore.isAuthenticated ? '/account' : '/login'" 
            class="p-2"
            aria-label="Account"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div 
      v-if="isMobileMenuOpen" 
      class="lg:hidden bg-white border-t border-gray-100 py-4"
    >
      <div class="container-custom">
        <nav class="flex flex-col space-y-4">
          <RouterLink 
            v-for="link in navLinks" 
            :key="link.path"
            :to="link.path"
            class="text-gray-700 hover:text-black transition-colors py-2"
            @click="isMobileMenuOpen = false"
          >
            {{ link.name }}
          </RouterLink>
        </nav>
      </div>
    </div>
  </header>
</template>
