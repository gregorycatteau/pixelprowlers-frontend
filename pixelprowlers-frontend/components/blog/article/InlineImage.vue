<template>
  <figure class="inline-image-figure"> 
    <img :src="src" :alt="alt" class="inline-image-img" />
    <figcaption v-if="caption" class="inline-image-caption">{{ caption }}</figcaption>
  </figure>
</template>

<script setup lang="ts">
defineProps<{ src: string; alt: string; caption?: string }>()
</script>

<style scoped>
@reference "@/assets/css/main.css";

.inline-image-figure {
  @apply flex flex-col items-center my-10;
}

.inline-image-img {
  @apply w-full max-w-4xl rounded-2xl shadow-lg transition hover:scale-105 duration-300 object-cover;
}

.inline-image-caption {
  @apply mt-3 text-sm text-gray-500 dark:text-gray-400 text-center max-w-2xl;
}
</style>

