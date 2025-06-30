<template>
  <section :id="id" class="section-block">
    <div class="section-content">
      <h2 class="section-title">{{ title }}</h2>
      <div class="section-body" v-html="safeContent" />
      <InlineImage v-if="image" :src="image" :alt="title" class="section-image" />
    </div>
  </section>
</template>

<script setup lang="ts">
import DOMPurify from 'dompurify'
import InlineImage from './InlineImage.vue'

const props = defineProps<{ id: string; title: string; content: string; image?: string }>()

const safeContent = DOMPurify.sanitize(props.content)
</script>

<style scoped>
@reference "@/assets/css/main.css";

.section-block {
  @apply bg-white dark:bg-neutral-900 shadow-sm hover:shadow-md rounded-2xl transition duration-300 mb-16 p-6 md:p-10;
}

.section-content {
  @apply space-y-6;
}

.section-title {
  @apply text-3xl font-bold text-neutral-900 dark:text-white leading-tight tracking-tight;
}

.section-body {
  @apply prose prose-lg dark:prose-invert max-w-none leading-relaxed;
}

.section-image {
  @apply mt-6;
}
</style>
