<template>
  <section v-if="notes.length" class="footnotes-block">
    <h3 class="footnotes-title">Notes</h3>
    <ol class="footnotes-list">
      <li
        v-for="note in notes"
        :key="note.order"
        v-html="sanitize(note.text)"
        class="footnotes-item"
      ></li>
    </ol>
  </section>
</template>

<script setup lang="ts">
import DOMPurify from 'dompurify'

const props = defineProps<{ notes: { text: string; order: number }[] }>()

function sanitize(text: string) {
  return DOMPurify.sanitize(text)
}
</script>

<style scoped>
@reference "@/assets/css/main.css";

.footnotes-block {
  @apply mt-20 bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-700 rounded-2xl p-6 md:p-10 space-y-6;
}

.footnotes-title {
  @apply text-xl font-semibold text-gray-900 dark:text-white;
}

.footnotes-list {
  @apply list-decimal ml-6 space-y-4;
}

.footnotes-item {
  @apply text-base text-gray-600 dark:text-gray-300 leading-relaxed;
}
</style>
