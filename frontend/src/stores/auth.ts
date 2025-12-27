import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { authApi } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  async function register(email: string, password: string, fullName?: string) {
    loading.value = true
    try {
      const response = await authApi.register(email, password, fullName)
      token.value = response.access_token
      localStorage.setItem('token', response.access_token)
      await fetchUser()
    } finally {
      loading.value = false
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    try {
      const response = await authApi.login(email, password)
      token.value = response.access_token
      localStorage.setItem('token', response.access_token)
      await fetchUser()
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      user.value = await authApi.getMe()
    } catch {
      logout()
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  // Initialize
  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    register,
    login,
    logout,
    fetchUser,
  }
})
