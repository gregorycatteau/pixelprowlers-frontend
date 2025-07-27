<template>
  <ScrollLayout />
</template>

<script setup lang="ts">
import ScrollLayout from '@/components/animation/ScrollLayout.vue'
import { useHead } from 'nuxt/app'   // ← import corrigé

useHead({
  title: 'Pixelprowlers.io | Le web éthique pour tous',
  meta: [
    {
      name: 'description',
      content: 'Pixelprowlers.io - Créateur de solutions web éthiques, accessibles et sécurisées.'
    }
  ]
})
</script>


