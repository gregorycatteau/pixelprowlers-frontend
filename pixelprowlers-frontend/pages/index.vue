<template>
  <ScrollLayout />
</template>

<script setup lang="ts">
definePageMeta({ ssr: false }) // désactive le SSR

import ScrollLayout from "@/components/animation/ScrollLayout.vue";
</script>