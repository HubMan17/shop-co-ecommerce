import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/shop',
      name: 'shop',
      component: () => import('@/views/CatalogView.vue'),
    },
    {
      path: '/shop/:category',
      name: 'category',
      component: () => import('@/views/CatalogView.vue'),
    },
    {
      path: '/product/:slug',
      name: 'product',
      component: () => import('@/views/ProductView.vue'),
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('@/views/CartView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
