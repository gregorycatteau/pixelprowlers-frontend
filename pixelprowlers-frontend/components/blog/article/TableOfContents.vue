<template>
  <div class="toc-block">
    <h3 class="toc-title">Sommaire</h3>
    <ul class="toc-list">
      <li v-for="item in items" :key="item.id">
        <a :href="`#${item.id}`" class="toc-link">{{ item.title }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
defineProps<{ items: { id: string; title: string }[] }>()
</script>

<style scoped>
@reference "@/assets/css/main.css";

.toc-block {
  @apply bg-neutral-900 text-white rounded-xl p-4 shadow-md;
}

.toc-title {
  @apply font-bold text-lg mb-4;
}

.toc-list {
  @apply flex flex-col space-y-2;
}

.toc-link {
  @apply text-sm text-gray-300 hover:text-white transition-colors;
}
</style>
