/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'satoshi': ['Satoshi', 'sans-serif'],
        'integral': ['Integral CF', 'sans-serif'],
      },
      colors: {
        'primary': '#000000',
        'secondary': '#F0F0F0',
        'accent': '#F97316',
        'muted': '#6B7280',
      },
    },
  },
  plugins: [],
}
