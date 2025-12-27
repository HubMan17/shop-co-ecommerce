<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const fullName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')

async function handleSubmit() {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }

  try {
    await authStore.register(email.value, password.value, fullName.value)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Registration failed. Please try again.'
  }
}
</script>

<template>
  <div class="min-h-[80vh] flex items-center justify-center py-12">
    <div class="w-full max-w-md px-4">
      <div class="text-center mb-8">
        <h1 class="heading-lg mb-2">Create Account</h1>
        <p class="text-gray-600">Join us and start shopping</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div v-if="error" class="bg-red-50 text-red-500 p-4 rounded-lg text-sm">
          {{ error }}
        </div>

        <div>
          <label for="fullName" class="block text-sm font-medium mb-2">Full Name</label>
          <input
            id="fullName"
            v-model="fullName"
            type="text"
            class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Enter your full name"
          />
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
            placeholder="Create a password"
          />
        </div>

        <div>
          <label for="confirmPassword" class="block text-sm font-medium mb-2">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Confirm your password"
          />
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="btn-primary w-full disabled:opacity-50"
        >
          {{ authStore.loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="text-center mt-6 text-gray-600">
        Already have an account?
        <RouterLink to="/login" class="font-medium text-black hover:underline">
          Sign In
        </RouterLink>
      </p>
    </div>
  </div>
</template>
