<script setup lang="ts">
import type { Product } from '@/types'
import StarRating from './StarRating.vue'

const props = defineProps<{
  product: Product
}>()

const primaryImage = props.product.images.find(img => img.is_primary)?.url || props.product.images[0]?.url || ''
const effectivePrice = props.product.discount_price || props.product.price
</script>

<template>
  <RouterLink :to="`/product/${product.slug}`" class="group block">
    <div class="bg-gray-100 rounded-2xl overflow-hidden aspect-square mb-4 relative">
      <img
        :src="primaryImage"
        :alt="product.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <span
        v-if="product.discount_percent"
        class="absolute top-3 right-3 bg-red-500 text-white text-xs font-medium px-2 py-1 rounded-full"
      >
        -{{ product.discount_percent }}%
      </span>
    </div>
    <h3 class="font-medium text-lg mb-1 group-hover:text-gray-600 transition-colors line-clamp-1">
      {{ product.name }}
    </h3>
    <StarRating :rating="product.rating" :reviews="product.reviews_count" class="mb-2" />
    <div class="flex items-center gap-2">
      <span class="font-bold text-xl">${{ effectivePrice }}</span>
      <span v-if="product.discount_price" class="text-gray-400 line-through">
        ${{ product.price }}
      </span>
      <span
        v-if="product.discount_percent"
        class="bg-red-100 text-red-500 text-xs font-medium px-2 py-1 rounded-full"
      >
        -{{ product.discount_percent }}%
      </span>
    </div>
  </RouterLink>
</template>
