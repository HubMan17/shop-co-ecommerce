export interface ColorOption {
  name: string
  hex: string
}

export interface ProductImage {
  id: number
  url: string
  is_primary: boolean
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  image_url?: string
}

export interface Product {
  id: number
  name: string
  slug: string
  description?: string
  price: number
  discount_price?: number
  discount_percent?: number
  sizes: string[]
  colors: ColorOption[]
  rating: number
  reviews_count: number
  stock: number
  is_new_arrival: boolean
  is_top_selling: boolean
  style?: string
  images: ProductImage[]
  category?: Category
  created_at: string
}

export interface ProductListResponse {
  items: Product[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface CartItem {
  id: number
  product_id: number
  product_name: string
  product_image?: string
  price: number
  discount_price?: number
  quantity: number
  size?: string
  color?: string
  subtotal: number
}

export interface Cart {
  id: number
  items: CartItem[]
  items_count: number
  subtotal: number
  discount: number
  delivery_fee: number
  total: number
}

export interface User {
  id: number
  email: string
  full_name?: string
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}
