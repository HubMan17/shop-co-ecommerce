import axios from 'axios'
import type { Product, ProductListResponse, Category, Cart, User, AuthResponse } from '@/types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authApi = {
  register: async (email: string, password: string, fullName?: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', { email, password, full_name: fullName })
    return response.data
  },

  login: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  getMe: async (): Promise<User> => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

// Products API
export const productsApi = {
  getProducts: async (params?: {
    page?: number
    per_page?: number
    category?: string
    style?: string
    min_price?: number
    max_price?: number
    search?: string
    sort?: string
  }): Promise<ProductListResponse> => {
    const response = await api.get('/products', { params })
    return response.data
  },

  getProduct: async (slug: string): Promise<Product> => {
    const response = await api.get(`/products/${slug}`)
    return response.data
  },

  getNewArrivals: async (limit = 4): Promise<Product[]> => {
    const response = await api.get('/products/new-arrivals', { params: { limit } })
    return response.data
  },

  getTopSelling: async (limit = 4): Promise<Product[]> => {
    const response = await api.get('/products/top-selling', { params: { limit } })
    return response.data
  },
}

// Categories API
export const categoriesApi = {
  getCategories: async (): Promise<Category[]> => {
    const response = await api.get('/categories')
    return response.data
  },

  getCategory: async (slug: string): Promise<Category> => {
    const response = await api.get(`/categories/${slug}`)
    return response.data
  },
}

// Cart API
export const cartApi = {
  getCart: async (): Promise<Cart> => {
    const response = await api.get('/cart')
    return response.data
  },

  addItem: async (productId: number, quantity = 1, size?: string, color?: string): Promise<Cart> => {
    const response = await api.post('/cart/items', {
      product_id: productId,
      quantity,
      size,
      color,
    })
    return response.data
  },

  updateItem: async (itemId: number, quantity: number): Promise<Cart> => {
    const response = await api.put(`/cart/items/${itemId}`, { quantity })
    return response.data
  },

  removeItem: async (itemId: number): Promise<Cart> => {
    const response = await api.delete(`/cart/items/${itemId}`)
    return response.data
  },
}

export default api
