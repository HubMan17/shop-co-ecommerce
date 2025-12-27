<script setup lang="ts">
import TheHeader from '@/components/layout/TheHeader.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
import TopBanner from '@/components/layout/TopBanner.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <TopBanner />
    <TheHeader />
    <main class="flex-1">
      <RouterView />
    </main>
    <TheFooter />
  </div>
</template>
