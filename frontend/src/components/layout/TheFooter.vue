<script setup lang="ts">
const footerLinks = {
  company: [
    { name: 'About', path: '/about' },
    { name: 'Features', path: '/features' },
    { name: 'Works', path: '/works' },
    { name: 'Career', path: '/career' },
  ],
  help: [
    { name: 'Customer Support', path: '/support' },
    { name: 'Delivery Details', path: '/delivery' },
    { name: 'Terms and Conditions', path: '/terms' },
    { name: 'Privacy Policy', path: '/privacy' },
  ],
  faq: [
    { name: 'Account', path: '/faq/account' },
    { name: 'Manage Deliveries', path: '/faq/deliveries' },
    { name: 'Orders', path: '/faq/orders' },
    { name: 'Payments', path: '/faq/payments' },
  ],
  resources: [
    { name: 'Free eBooks', path: '/resources/ebooks' },
    { name: 'Development Tutorial', path: '/resources/tutorials' },
    { name: 'How to - Blog', path: '/blog' },
    { name: 'Youtube Playlist', path: '/resources/youtube' },
  ],
}

const socialLinks = [
  { name: 'Twitter', icon: 'twitter', url: '#' },
  { name: 'Facebook', icon: 'facebook', url: '#' },
  { name: 'Instagram', icon: 'instagram', url: '#' },
  { name: 'Github', icon: 'github', url: '#' },
]
</script>

<template>
  <footer class="bg-gray-100 pt-16 pb-8">
    <!-- Newsletter Section -->
    <div class="container-custom mb-12">
      <div class="bg-black rounded-3xl p-8 md:p-12 flex flex-col md:flex-row items-center justify-between gap-6">
        <h2 class="heading-lg text-white text-center md:text-left max-w-lg">
          STAY UPTO DATE ABOUT OUR LATEST OFFERS
        </h2>
        <div class="w-full md:w-auto">
          <form class="flex flex-col gap-3 w-full md:w-80">
            <div class="relative">
              <input
                type="email"
                placeholder="Enter your email address"
                class="w-full bg-white rounded-full py-3 pl-12 pr-4 text-sm focus:outline-none"
              />
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <button type="submit" class="bg-white text-black rounded-full py-3 px-6 font-medium hover:bg-gray-100 transition-colors">
              Subscribe to Newsletter
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- Footer Links -->
    <div class="container-custom">
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8 pb-12 border-b border-gray-300">
        <!-- Brand -->
        <div class="col-span-2 md:col-span-3 lg:col-span-1">
          <RouterLink to="/" class="text-2xl font-bold mb-4 block" style="font-family: Integral CF, sans-serif;">
            SHOP.CO
          </RouterLink>
          <p class="text-gray-600 text-sm mb-6">
            We have clothes that suits your style and which you are proud to wear. From women to men.
          </p>
          <div class="flex space-x-3">
            <a
              v-for="social in socialLinks"
              :key="social.name"
              :href="social.url"
              class="w-8 h-8 bg-white border border-gray-300 rounded-full flex items-center justify-center hover:bg-black hover:text-white hover:border-black transition-all"
              :aria-label="social.name"
            >
              <svg v-if="social.icon === 'twitter'" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              <svg v-if="social.icon === 'facebook'" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              <svg v-if="social.icon === 'instagram'" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
              <svg v-if="social.icon === 'github'" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            </a>
          </div>
        </div>

        <!-- Company -->
        <div>
          <h3 class="font-medium text-sm tracking-wider mb-4">COMPANY</h3>
          <ul class="space-y-3">
            <li v-for="link in footerLinks.company" :key="link.path">
              <RouterLink :to="link.path" class="text-gray-600 text-sm hover:text-black transition-colors">
                {{ link.name }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Help -->
        <div>
          <h3 class="font-medium text-sm tracking-wider mb-4">HELP</h3>
          <ul class="space-y-3">
            <li v-for="link in footerLinks.help" :key="link.path">
              <RouterLink :to="link.path" class="text-gray-600 text-sm hover:text-black transition-colors">
                {{ link.name }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- FAQ -->
        <div>
          <h3 class="font-medium text-sm tracking-wider mb-4">FAQ</h3>
          <ul class="space-y-3">
            <li v-for="link in footerLinks.faq" :key="link.path">
              <RouterLink :to="link.path" class="text-gray-600 text-sm hover:text-black transition-colors">
                {{ link.name }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Resources -->
        <div>
          <h3 class="font-medium text-sm tracking-wider mb-4">RESOURCES</h3>
          <ul class="space-y-3">
            <li v-for="link in footerLinks.resources" :key="link.path">
              <RouterLink :to="link.path" class="text-gray-600 text-sm hover:text-black transition-colors">
                {{ link.name }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-gray-600 text-sm">
          Shop.co 2024, All Rights Reserved
        </p>
        <div class="flex items-center space-x-3">
          <div class="bg-white rounded px-2 py-1 text-xs font-bold text-blue-600">VISA</div>
          <div class="bg-white rounded px-2 py-1 text-xs font-bold text-red-500">MC</div>
          <div class="bg-white rounded px-2 py-1 text-xs font-bold text-blue-500">PayPal</div>
          <div class="bg-white rounded px-2 py-1 text-xs font-bold">Apple</div>
          <div class="bg-white rounded px-2 py-1 text-xs font-bold">GPay</div>
        </div>
      </div>
    </div>
  </footer>
</template>
