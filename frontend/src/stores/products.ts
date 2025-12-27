import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Product, ProductListResponse, Category } from '@/types'
import { productsApi, categoriesApi } from '@/services/api'

export const useProductsStore = defineStore('products', () => {
  const products = ref<Product[]>([])
  const currentProduct = ref<Product | null>(null)
  const categories = ref<Category[]>([])
  const newArrivals = ref<Product[]>([])
  const topSelling = ref<Product[]>([])
  const loading = ref(false)
  const pagination = ref({
    total: 0,
    page: 1,
    per_page: 12,
    pages: 0,
  })

  async function fetchProducts(params?: {
    page?: number
    per_page?: number
    category?: string
    style?: string
    min_price?: number
    max_price?: number
    search?: string
    sort?: string
  }) {
    loading.value = true
    try {
      const response = await productsApi.getProducts(params)
      products.value = response.items
      pagination.value = {
        total: response.total,
        page: response.page,
        per_page: response.per_page,
        pages: response.pages,
      }
    } finally {
      loading.value = false
    }
  }

  async function fetchProduct(slug: string) {
    loading.value = true
    try {
      currentProduct.value = await productsApi.getProduct(slug)
    } finally {
      loading.value = false
    }
  }

  async function fetchNewArrivals(limit = 4) {
    try {
      newArrivals.value = await productsApi.getNewArrivals(limit)
    } catch (error) {
      console.error('Failed to fetch new arrivals:', error)
    }
  }

  async function fetchTopSelling(limit = 4) {
    try {
      topSelling.value = await productsApi.getTopSelling(limit)
    } catch (error) {
      console.error('Failed to fetch top selling:', error)
    }
  }

  async function fetchCategories() {
    try {
      categories.value = await categoriesApi.getCategories()
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  }

  return {
    products,
    currentProduct,
    categories,
    newArrivals,
    topSelling,
    loading,
    pagination,
    fetchProducts,
    fetchProduct,
    fetchNewArrivals,
    fetchTopSelling,
    fetchCategories,
  }
})
