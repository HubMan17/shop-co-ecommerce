<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')

async function handleSubmit() {
  error.value = ''
  try {
    await authStore.login(email.value, password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Login failed. Please try again.'
  }
}
</script>

<template>
  <div class="min-h-[80vh] flex items-center justify-center py-12">
    <div class="w-full max-w-md px-4">
      <div class="text-center mb-8">
        <h1 class="heading-lg mb-2">Welcome Back</h1>
        <p class="text-gray-600">Sign in to your account</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div v-if="error" class="bg-red-50 text-red-500 p-4 rounded-lg text-sm">
          {{ error }}
        </div>

        <div>
          <label for="email" class="block text-sm font-medium mb-2">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Enter your email"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium mb-2">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Enter your password"
          />
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="btn-primary w-full disabled:opacity-50"
        >
          {{ authStore.loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <p class="text-center mt-6 text-gray-600">
        Do not have an account?
        <RouterLink to="/register" class="font-medium text-black hover:underline">
          Sign Up
        </RouterLink>
      </p>
    </div>
  </div>
</template>
