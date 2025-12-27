<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import ProductCard from '@/components/ui/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const productsStore = useProductsStore()

const showFilters = ref(false)
const priceRange = ref([0, 500])
const selectedSizes = ref<string[]>([])
const selectedColors = ref<string[]>([])
const sortBy = ref('newest')

const sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
const colors = [
  { name: 'Black', hex: '#000000' },
  { name: 'White', hex: '#FFFFFF' },
  { name: 'Red', hex: '#DC2626' },
  { name: 'Blue', hex: '#2563EB' },
  { name: 'Green', hex: '#16A34A' },
  { name: 'Orange', hex: '#EA580C' },
]

const sortOptions = [
  { value: 'newest', label: 'Newest' },
  { value: 'price_low', label: 'Price: Low to High' },
  { value: 'price_high', label: 'Price: High to Low' },
  { value: 'popular', label: 'Most Popular' },
  { value: 'rating', label: 'Top Rated' },
]

const categorySlug = computed(() => route.params.category as string || '')
const searchQuery = computed(() => route.query.search as string || '')

async function fetchProducts() {
  await productsStore.fetchProducts({
    page: productsStore.pagination.page,
    per_page: 12,
    category: categorySlug.value,
    search: searchQuery.value,
    min_price: priceRange.value[0] > 0 ? priceRange.value[0] : undefined,
    max_price: priceRange.value[1] < 500 ? priceRange.value[1] : undefined,
    sort: sortBy.value,
  })
}

function applyFilters() {
  fetchProducts()
  showFilters.value = false
}

function changePage(page: number) {
  productsStore.pagination.page = page
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  productsStore.fetchCategories()
  fetchProducts()
})

watch([categorySlug, searchQuery], () => {
  productsStore.pagination.page = 1
  fetchProducts()
})

watch(sortBy, () => {
  fetchProducts()
})
</script>

<template>
  <div class="py-8">
    <div class="container-custom">
      <!-- Breadcrumbs -->
      <nav class="flex items-center gap-2 text-sm mb-8">
        <RouterLink to="/" class="text-gray-500 hover:text-black">Home</RouterLink>
        <span class="text-gray-400">/</span>
        <span class="font-medium">{{ categorySlug ? productsStore.categories.find(c => c.slug === categorySlug)?.name : 'Shop' }}</span>
      </nav>

      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Filters Sidebar -->
        <aside
          :class="[
            'lg:w-64 flex-shrink-0',
            showFilters ? 'fixed inset-0 z-50 bg-white p-6 overflow-y-auto lg:static lg:p-0' : 'hidden lg:block'
          ]"
        >
          <div class="flex items-center justify-between mb-6 lg:mb-0">
            <h2 class="text-xl font-bold lg:hidden">Filters</h2>
            <button @click="showFilters = false" class="lg:hidden">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="border border-gray-200 rounded-2xl p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="font-bold">Filters</h3>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
            </div>

            <!-- Categories -->
            <div class="border-t border-gray-200 py-6">
              <h4 class="font-medium mb-4">Categories</h4>
              <ul class="space-y-3">
                <li>
                  <RouterLink
                    to="/shop"
                    :class="['text-sm hover:text-black transition-colors', !categorySlug ? 'font-medium text-black' : 'text-gray-600']"
                  >
                    All Products
                  </RouterLink>
                </li>
                <li v-for="cat in productsStore.categories" :key="cat.id">
                  <RouterLink
                    :to="`/shop/${cat.slug}`"
                    :class="['text-sm hover:text-black transition-colors', categorySlug === cat.slug ? 'font-medium text-black' : 'text-gray-600']"
                  >
                    {{ cat.name }}
                  </RouterLink>
                </li>
              </ul>
            </div>

            <!-- Price Range -->
            <div class="border-t border-gray-200 py-6">
              <h4 class="font-medium mb-4">Price</h4>
              <div class="flex items-center gap-4">
                <input
                  v-model.number="priceRange[0]"
                  type="number"
                  min="0"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                  placeholder="Min"
                />
                <span class="text-gray-400">-</span>
                <input
                  v-model.number="priceRange[1]"
                  type="number"
                  min="0"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                  placeholder="Max"
                />
              </div>
            </div>

            <!-- Colors -->
            <div class="border-t border-gray-200 py-6">
              <h4 class="font-medium mb-4">Colors</h4>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="color in colors"
                  :key="color.name"
                  @click="selectedColors.includes(color.name) ? selectedColors = selectedColors.filter(c => c !== color.name) : selectedColors.push(color.name)"
                  :class="[
                    'w-8 h-8 rounded-full border-2 transition-all',
                    selectedColors.includes(color.name) ? 'ring-2 ring-offset-2 ring-black' : 'border-gray-300'
                  ]"
                  :style="{ backgroundColor: color.hex }"
                  :title="color.name"
                />
              </div>
            </div>

            <!-- Sizes -->
            <div class="border-t border-gray-200 py-6">
              <h4 class="font-medium mb-4">Size</h4>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="size in sizes"
                  :key="size"
                  @click="selectedSizes.includes(size) ? selectedSizes = selectedSizes.filter(s => s !== size) : selectedSizes.push(size)"
                  :class="[
                    'px-4 py-2 rounded-full text-sm font-medium transition-all',
                    selectedSizes.includes(size) ? 'bg-black text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ size }}
                </button>
              </div>
            </div>

            <!-- Apply Button -->
            <button @click="applyFilters" class="btn-primary w-full mt-4">
              Apply Filters
            </button>
          </div>
        </aside>

        <!-- Products Grid -->
        <div class="flex-1">
          <!-- Header -->
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
            <div>
              <h1 class="text-2xl font-bold">
                {{ categorySlug ? productsStore.categories.find(c => c.slug === categorySlug)?.name : 'All Products' }}
              </h1>
              <p class="text-gray-500 text-sm mt-1">
                Showing {{ productsStore.products.length }} of {{ productsStore.pagination.total }} products
              </p>
            </div>
            <div class="flex items-center gap-4 w-full sm:w-auto">
              <button
                @click="showFilters = true"
                class="lg:hidden flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                Filters
              </button>
              <select
                v-model="sortBy"
                class="flex-1 sm:flex-none border border-gray-300 rounded-lg px-4 py-2 text-sm bg-white"
              >
                <option v-for="option in sortOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="productsStore.loading" class="flex items-center justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
          </div>

          <!-- Products Grid -->
          <div v-else-if="productsStore.products.length > 0" class="grid grid-cols-2 md:grid-cols-3 gap-4 lg:gap-6">
            <ProductCard
              v-for="product in productsStore.products"
              :key="product.id"
              :product="product"
            />
          </div>

          <!-- No Products -->
          <div v-else class="text-center py-20">
            <p class="text-gray-500 text-lg">No products found</p>
            <RouterLink to="/shop" class="btn-primary inline-block mt-4">
              View All Products
            </RouterLink>
          </div>

          <!-- Pagination -->
          <div v-if="productsStore.pagination.pages > 1" class="flex items-center justify-center gap-2 mt-12">
            <button
              @click="changePage(productsStore.pagination.page - 1)"
              :disabled="productsStore.pagination.page === 1"
              class="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
            >
              Previous
            </button>
            <template v-for="page in productsStore.pagination.pages" :key="page">
              <button
                v-if="page === 1 || page === productsStore.pagination.pages || (page >= productsStore.pagination.page - 1 && page <= productsStore.pagination.page + 1)"
                @click="changePage(page)"
                :class="[
                  'w-10 h-10 rounded-lg transition-colors',
                  page === productsStore.pagination.page ? 'bg-black text-white' : 'hover:bg-gray-100'
                ]"
              >
                {{ page }}
              </button>
              <span v-else-if="page === productsStore.pagination.page - 2 || page === productsStore.pagination.page + 2" class="px-2">...</span>
            </template>
            <button
              @click="changePage(productsStore.pagination.page + 1)"
              :disabled="productsStore.pagination.page === productsStore.pagination.pages"
              class="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
