import tailwindcss from "@tailwindcss/vite";

// Détection de l'environnement courant
const environment = process.env.NODE_ENV || 'development';

export default defineNuxtConfig({
  future: {
    compatibilityVersion: 4
  },
  compatibilityDate: "2024-11-01",
  devtools: { enabled: environment === 'development' },

  // Chargement des variables d'environnement
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_API_BASE_URL || 'http://localhost:8000/api',
      siteName: process.env.NUXT_PUBLIC_SITE_NAME || 'Pixel Prowlers (Dev)',
    }
  },

  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
});
