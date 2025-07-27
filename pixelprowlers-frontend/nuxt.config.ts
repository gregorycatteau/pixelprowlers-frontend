import { defineNuxtConfig } from 'nuxt/config'
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",

  // --- Devtools ---
  devtools: {
    enabled: true,
    timeline: { enabled: true }
  },

  // --- CSS global ---
  css: ['~/assets/css/main.css'],

  // --- Vite & Tailwind ---
  vite: {
    plugins: [tailwindcss()],
  },

  // --- Modules ---
  modules: [
    // GSAP + options inline
    ['@hypernym/nuxt-gsap', {
      extraPlugins: {
        scrollTrigger: true,
        scrollTo:      true,
      }
    }],

    // VueUse (pas d’options spéciales)
    '@vueuse/nuxt',

    // Pinia + autoImport direct dans modules
    ['@pinia/nuxt', {
      autoImports: [
        'defineStore',
        'acceptHMRUpdate'
      ]
    }],
  ],

  // --- Dev Server (réseau local) ---
  devServer: {
    host: '0.0.0.0',
    port: 3000,
  },

  // --- Runtime Config ---
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_API_BASE_URL  || 'http://localhost:8000/api',
      siteName:   process.env.NUXT_PUBLIC_SITE_NAME || 'Pixel Prowlers (Dev)',
    },
  },
});

