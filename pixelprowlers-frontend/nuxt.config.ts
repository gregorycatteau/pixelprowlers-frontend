import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",

  devtools: { enabled: true },

  css: ['~/assets/css/main.css'],

  vite: {
    plugins: [tailwindcss()],
  },

  modules: [
    '@hypernym/nuxt-gsap',
    '@vueuse/nuxt',
  ],

  gsap: {
    extraPlugins: {
      scrollTrigger: true,
      scrollTo: true,
    },
  },

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_API_BASE_URL || 'http://localhost:8000/api',
      siteName: process.env.NUXT_PUBLIC_SITE_NAME || 'Pixel Prowlers (Dev)',
    },
  },
  routeRules: {
    '/blog/**': { ssr: true },
  }
  
});
