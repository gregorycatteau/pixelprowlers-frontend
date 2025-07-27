<template>
  <div :class="[pageClass, 'min-h-screen text-gray-900 dark:text-gray-100']">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useHead } from 'nuxt/app'
import { computed } from 'vue'

useHead({
  titleTemplate: (title) =>
    title ? `${title}` : 'Pixelprowlers.io | Le web éthique pour tous',
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    {
      name: 'description',
      content: 'Pixelprowlers.io - Création de sites web engagés, sécurisés et accessibles.'
    }
  ],
  link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
})

const route = useRoute()

const pageClass = computed(() => {
  // ✅ On applique le fond uniquement sur les pages d’articles dynamiques
  if (route.name === 'blog-slug') {
    return 'article-page-bg'
  }
  return ''
})
</script>

<style>
@reference "@/assets/css/main.css";

/* 🌌 Fond spécifique aux pages d’articles dynamiques */
.article-page-bg {
  background-image: url('/fond-ecran.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-repeat: no-repeat;
}
</style>


