<script setup lang="ts">
import { ref } from 'vue'

const isVisible = ref(true)
</script>

<template>
  <div v-if="isVisible" class="bg-black text-white py-2 text-center text-sm relative">
    <div class="container-custom">
      <p>
        Sign up and get 20% off to your first order. 
        <RouterLink to="/register" class="underline font-medium hover:text-gray-300">
          Sign Up Now
        </RouterLink>
      </p>
    </div>
    <button 
      @click="isVisible = false"
      class="absolute right-4 top-1/2 -translate-y-1/2 text-white hover:text-gray-300"
      aria-label="Close banner"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>
