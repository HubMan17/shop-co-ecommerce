<script setup lang="ts">
import { onMounted } from 'vue'
import { useProductsStore } from '@/stores/products'
import ProductCard from '@/components/ui/ProductCard.vue'

const productsStore = useProductsStore()

onMounted(() => {
  productsStore.fetchNewArrivals(4)
  productsStore.fetchTopSelling(4)
})

const brands = ['VERSACE', 'ZARA', 'GUCCI', 'PRADA', 'Calvin Klein']

const styles = [
  { name: 'Casual', image: 'https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=400', class: 'col-span-1 row-span-2' },
  { name: 'Formal', image: 'https://images.unsplash.com/photo-1507680434567-5739c80be1ac?w=400', class: 'col-span-1' },
  { name: 'Party', image: 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=400', class: 'col-span-1' },
  { name: 'Gym', image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400', class: 'col-span-1 row-span-2' },
]

const testimonials = [
  { name: 'Sarah M.', rating: 5, text: 'I am blown away by the quality and style of the clothes I received from Shop.co. From casual wear to elegant dresses, every piece I have bought has exceeded my expectations.', verified: true },
  { name: 'Alex K.', rating: 5, text: 'Finding clothes that align with my personal style used to be a challenge until I discovered Shop.co. The range of options they offer is truly remarkable, catering to a variety of tastes and occasions.', verified: true },
  { name: 'James L.', rating: 5, text: 'As someone who is always on the lookout for unique fashion pieces, I am thrilled to have stumbled upon Shop.co. The selection of clothes is not only diverse but also on-point with the latest trends.', verified: true },
]
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gray-100 overflow-hidden">
      <div class="container-custom">
        <div class="flex flex-col lg:flex-row items-center">
          <div class="py-12 lg:py-24 lg:w-1/2">
            <h1 class="heading-xl mb-6">
              FIND CLOTHES THAT MATCHES YOUR STYLE
            </h1>
            <p class="text-gray-600 mb-8 max-w-lg">
              Browse through our diverse range of meticulously crafted garments, designed to bring out your individuality and cater to your sense of style.
            </p>
            <RouterLink to="/shop" class="btn-primary inline-block">
              Shop Now
            </RouterLink>
            <div class="flex flex-wrap gap-8 mt-12">
              <div>
                <p class="text-3xl lg:text-4xl font-bold">200+</p>
                <p class="text-gray-600 text-sm">International Brands</p>
              </div>
              <div class="border-l border-gray-300 pl-8">
                <p class="text-3xl lg:text-4xl font-bold">2,000+</p>
                <p class="text-gray-600 text-sm">High-Quality Products</p>
              </div>
              <div class="border-l border-gray-300 pl-8">
                <p class="text-3xl lg:text-4xl font-bold">30,000+</p>
                <p class="text-gray-600 text-sm">Happy Customers</p>
              </div>
            </div>
          </div>
          <div class="lg:w-1/2 relative">
            <img
              src="https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800"
              alt="Fashion models"
              class="w-full h-[400px] lg:h-[600px] object-cover"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Brands Strip -->
    <section class="bg-black py-6">
      <div class="container-custom">
        <div class="flex flex-wrap justify-center lg:justify-between items-center gap-6 lg:gap-12">
          <span v-for="brand in brands" :key="brand" class="text-white text-xl lg:text-2xl font-bold opacity-80">
            {{ brand }}
          </span>
        </div>
      </div>
    </section>

    <!-- New Arrivals -->
    <section class="py-16">
      <div class="container-custom">
        <h2 class="heading-lg text-center mb-12">NEW ARRIVALS</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 lg:gap-6">
          <ProductCard
            v-for="product in productsStore.newArrivals"
            :key="product.id"
            :product="product"
          />
        </div>
        <div class="text-center mt-8">
          <RouterLink to="/shop?filter=new" class="btn-secondary inline-block">
            View All
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Divider -->
    <div class="container-custom">
      <hr class="border-gray-200" />
    </div>

    <!-- Top Selling -->
    <section class="py-16">
      <div class="container-custom">
        <h2 class="heading-lg text-center mb-12">TOP SELLING</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 lg:gap-6">
          <ProductCard
            v-for="product in productsStore.topSelling"
            :key="product.id"
            :product="product"
          />
        </div>
        <div class="text-center mt-8">
          <RouterLink to="/shop?sort=popular" class="btn-secondary inline-block">
            View All
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Browse by Style -->
    <section class="py-16 bg-gray-100">
      <div class="container-custom">
        <div class="bg-gray-100 rounded-3xl p-8 lg:p-16">
          <h2 class="heading-lg text-center mb-12">BROWSE BY DRESS STYLE</h2>
          <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
            <RouterLink
              v-for="style in styles"
              :key="style.name"
              :to="`/shop?style=${style.name.toLowerCase()}`"
              :class="[style.class, 'relative rounded-2xl overflow-hidden group min-h-[200px] lg:min-h-[280px]']"
            >
              <img
                :src="style.image"
                :alt="style.name"
                class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
              <span class="absolute bottom-4 left-4 text-white text-xl lg:text-2xl font-bold">
                {{ style.name }}
              </span>
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="py-16">
      <div class="container-custom">
        <h2 class="heading-lg text-center mb-12">OUR HAPPY CUSTOMERS</h2>
        <div class="grid md:grid-cols-3 gap-6">
          <div
            v-for="testimonial in testimonials"
            :key="testimonial.name"
            class="bg-white border border-gray-200 rounded-2xl p-6"
          >
            <div class="flex mb-4">
              <svg v-for="i in testimonial.rating" :key="i" class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <div class="flex items-center gap-2 mb-3">
              <span class="font-bold">{{ testimonial.name }}</span>
              <svg v-if="testimonial.verified" class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <p class="text-gray-600 text-sm">{{ testimonial.text }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
