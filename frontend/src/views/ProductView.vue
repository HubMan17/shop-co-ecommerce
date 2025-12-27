<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import StarRating from '@/components/ui/StarRating.vue'

const route = useRoute()
const productsStore = useProductsStore()
const cartStore = useCartStore()

const selectedSize = ref('')
const selectedColor = ref('')
const quantity = ref(1)
const activeTab = ref('details')
const currentImageIndex = ref(0)
const addingToCart = ref(false)

const product = computed(() => productsStore.currentProduct)
const effectivePrice = computed(() => product.value?.discount_price || product.value?.price || 0)

const tabs = [
  { id: 'details', label: 'Product Details' },
  { id: 'reviews', label: 'Rating & Reviews' },
  { id: 'faqs', label: 'FAQs' },
]

async function addToCart() {
  if (!product.value || !selectedSize.value) return
  addingToCart.value = true
  try {
    await cartStore.addItem(product.value.id, quantity.value, selectedSize.value, selectedColor.value)
    alert('Added to cart!')
  } catch (error) {
    alert('Failed to add to cart')
  } finally {
    addingToCart.value = false
  }
}

function decrementQuantity() {
  if (quantity.value > 1) quantity.value--
}

function incrementQuantity() {
  quantity.value++
}

onMounted(() => {
  const slug = route.params.slug as string
  productsStore.fetchProduct(slug)
})

watch(() => route.params.slug, (newSlug) => {
  if (newSlug) {
    productsStore.fetchProduct(newSlug as string)
    selectedSize.value = ''
    selectedColor.value = ''
    quantity.value = 1
    currentImageIndex.value = 0
  }
})

watch(product, (newProduct) => {
  if (newProduct?.colors?.length) {
    selectedColor.value = newProduct.colors[0].name
  }
})
</script>

<template>
  <div class="py-8">
    <div class="container-custom">
      <!-- Breadcrumbs -->
      <nav class="flex items-center gap-2 text-sm mb-8">
        <RouterLink to="/" class="text-gray-500 hover:text-black">Home</RouterLink>
        <span class="text-gray-400">/</span>
        <RouterLink to="/shop" class="text-gray-500 hover:text-black">Shop</RouterLink>
        <span class="text-gray-400">/</span>
        <span class="font-medium">{{ product?.name }}</span>
      </nav>

      <!-- Loading -->
      <div v-if="productsStore.loading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
      </div>

      <template v-else-if="product">
        <div class="grid lg:grid-cols-2 gap-8 lg:gap-12">
          <!-- Image Gallery -->
          <div class="flex flex-col-reverse lg:flex-row gap-4">
            <!-- Thumbnails -->
            <div class="flex lg:flex-col gap-3 overflow-x-auto lg:overflow-visible">
              <button
                v-for="(image, index) in product.images"
                :key="image.id"
                @click="currentImageIndex = index"
                :class="[
                  'flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all',
                  currentImageIndex === index ? 'border-black' : 'border-gray-200'
                ]"
              >
                <img :src="image.url" :alt="product.name" class="w-full h-full object-cover" />
              </button>
            </div>

            <!-- Main Image -->
            <div class="flex-1 bg-gray-100 rounded-2xl overflow-hidden aspect-square">
              <img
                :src="product.images[currentImageIndex]?.url"
                :alt="product.name"
                class="w-full h-full object-cover"
              />
            </div>
          </div>

          <!-- Product Info -->
          <div>
            <h1 class="heading-lg mb-4">{{ product.name }}</h1>

            <StarRating :rating="product.rating" :reviews="product.reviews_count" class="mb-4" />

            <div class="flex items-center gap-3 mb-6">
              <span class="text-3xl font-bold">${{ effectivePrice }}</span>
              <span v-if="product.discount_price" class="text-2xl text-gray-400 line-through">
                ${{ product.price }}
              </span>
              <span
                v-if="product.discount_percent"
                class="bg-red-100 text-red-500 text-sm font-medium px-3 py-1 rounded-full"
              >
                -{{ product.discount_percent }}%
              </span>
            </div>

            <p class="text-gray-600 mb-6 border-b border-gray-200 pb-6">
              {{ product.description }}
            </p>

            <!-- Color Selector -->
            <div class="mb-6 border-b border-gray-200 pb-6">
              <h3 class="text-sm font-medium mb-3">Select Colors</h3>
              <div class="flex gap-3">
                <button
                  v-for="color in product.colors"
                  :key="color.name"
                  @click="selectedColor = color.name"
                  :class="[
                    'w-10 h-10 rounded-full border-2 transition-all relative',
                    selectedColor === color.name ? 'ring-2 ring-offset-2 ring-black' : 'border-gray-300'
                  ]"
                  :style="{ backgroundColor: color.hex }"
                  :title="color.name"
                >
                  <svg
                    v-if="selectedColor === color.name"
                    class="absolute inset-0 m-auto w-5 h-5"
                    :class="color.hex === '#FFFFFF' || color.hex === '#ffffff' ? 'text-black' : 'text-white'"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Size Selector -->
            <div class="mb-6 border-b border-gray-200 pb-6">
              <h3 class="text-sm font-medium mb-3">Choose Size</h3>
              <div class="flex flex-wrap gap-3">
                <button
                  v-for="size in product.sizes"
                  :key="size"
                  @click="selectedSize = size"
                  :class="[
                    'px-6 py-3 rounded-full text-sm font-medium transition-all',
                    selectedSize === size ? 'bg-black text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ size }}
                </button>
              </div>
            </div>

            <!-- Quantity and Add to Cart -->
            <div class="flex gap-4">
              <div class="flex items-center border border-gray-300 rounded-full">
                <button
                  @click="decrementQuantity"
                  class="w-12 h-12 flex items-center justify-center text-xl hover:bg-gray-100 rounded-l-full"
                >
                  -
                </button>
                <span class="w-12 text-center font-medium">{{ quantity }}</span>
                <button
                  @click="incrementQuantity"
                  class="w-12 h-12 flex items-center justify-center text-xl hover:bg-gray-100 rounded-r-full"
                >
                  +
                </button>
              </div>
              <button
                @click="addToCart"
                :disabled="!selectedSize || addingToCart"
                class="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Tabs Section -->
        <div class="mt-16">
          <div class="flex border-b border-gray-200">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'flex-1 py-4 text-center font-medium transition-colors relative',
                activeTab === tab.id ? 'text-black' : 'text-gray-500 hover:text-black'
              ]"
            >
              {{ tab.label }}
              <span
                v-if="activeTab === tab.id"
                class="absolute bottom-0 left-0 right-0 h-0.5 bg-black"
              />
            </button>
          </div>

          <div class="py-8">
            <div v-if="activeTab === 'details'">
              <p class="text-gray-600 leading-relaxed">{{ product.description }}</p>
              <ul class="mt-4 space-y-2">
                <li class="flex items-center gap-2">
                  <span class="font-medium">Category:</span>
                  <span class="text-gray-600">{{ product.category?.name }}</span>
                </li>
                <li class="flex items-center gap-2">
                  <span class="font-medium">Style:</span>
                  <span class="text-gray-600 capitalize">{{ product.style }}</span>
                </li>
                <li class="flex items-center gap-2">
                  <span class="font-medium">In Stock:</span>
                  <span class="text-gray-600">{{ product.stock }} items</span>
                </li>
              </ul>
            </div>

            <div v-else-if="activeTab === 'reviews'" class="text-center py-8">
              <p class="text-gray-500">No reviews yet. Be the first to review this product!</p>
            </div>

            <div v-else-if="activeTab === 'faqs'" class="text-center py-8">
              <p class="text-gray-500">No FAQs available for this product.</p>
            </div>
          </div>
        </div>
      </template>

      <!-- Not Found -->
      <div v-else class="text-center py-20">
        <p class="text-gray-500 text-lg">Product not found</p>
        <RouterLink to="/shop" class="btn-primary inline-block mt-4">
          View All Products
        </RouterLink>
      </div>
    </div>
  </div>
</template>
