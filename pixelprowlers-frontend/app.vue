<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useHead } from 'nuxt/app'

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
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
  ]
})
</script>

<style scoped></style>

