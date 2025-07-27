<template>
  <section :id="id" class="section-block">
    <div class="section-content">
      <h2 v-if="title" class="section-title">{{ title }}</h2>

      <div
        class="section-body prose dark:prose-invert prose-lg max-w-none"
        v-html="safeContent"
      />

      <InlineImage
        v-if="image"
        :src="image"
        :alt="title || 'Image sans titre'"
        class="section-image"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import DOMPurify from 'dompurify'
import InlineImage from './InlineImage.vue'

const props = defineProps<{
  id: string
  title?: string
  content: string
  image?: string
}>()
console.log('🔍 SectionBlock — contenu brut reçu :', props.content)
// ✅ Assainir le HTML pour éviter les XSS
const safeContent = DOMPurify.sanitize(props.content)
</script>

<style scoped>
@reference "@/assets/css/main.css";

/* Conteneur principal */
.section-block {
  @apply  bg-gray-900/95 shadow-sm rounded-2xl transition duration-300 mb-4 p-2 md:p-10;
}

.section-content {
  @apply space-y-2 ;
}

.section-title {
  @apply text-3xl font-bold text-primary dark:text-white leading-tight tracking-tight;
}

/* Zone injectée par v-html */
.section-body {
  @apply max-w-none opacity-50  p-4 rounded-lg shadow-inner;
}

.section-body :deep(*) {
  @apply leading-relaxed break-words;
}

/* TITRES */
.section-body :deep(h1) {
  @apply text-4xl font-bold mb-6 mt-8 text-red-600 dark:prose-zinc;
}
.section-body :deep(h2) {
  @apply text-3xl font-semibold mb-5 mt-8 text-alert ;
}
.section-body :deep(h3) {
  @apply text-2xl font-medium mb-4 mt-6 text-primary dark:text-white;
}
.section-body :deep(h4) {
  @apply text-xl font-medium mb-3 mt-5 text-primary dark:text-white;
}
.prose :where(h1, h2, h3) {
  @apply text-center max-w-3xl mx-auto leading-tight;
}
/* PARAGRAPHES */
.section-body :deep(p) {
  @apply text-base text-accent dark:text-cyan-500 mb-5;
}
.prose :where(p) {
  @apply text-justify indent-6 mb-5;
}
/* LISTES */
.section-body :deep(ul) {
  @apply list-disc list-inside text-base text-alert mb-5;
}
.section-body :deep(ol) {
  @apply list-decimal list-inside text-base text-gray-800 dark:text-gray-300 mb-5;
}
.section-body :deep(li) {
  @apply mb-2;
}

/* LIENS */
.section-body :deep(a) {
  @apply text-blue-600 dark:text-blue-400 underline hover:text-blue-800 dark:hover:text-blue-200 transition;
}

/* CITATIONS */
.section-body :deep(blockquote) {
  @apply border-l-4 border-gray-400 dark:border-gray-600 pl-4 italic text-accent dark:text-gray-300 mb-6;
}

/* CODES */
.section-body :deep(code) {
  @apply font-mono text-sm bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded;
}
.section-body :deep(pre) {
  @apply bg-gray-100 dark:bg-gray-800 text-sm p-4 rounded overflow-x-auto mb-6;
}

/* EMPHASIS */
.section-body :deep(em) {
  @apply italic;
}
.section-body :deep(strong) {
  @apply font-semibold text-black dark:text-white;
}

/* HR */
.section-body :deep(hr) {
  @apply border-t border-gray-300 dark:border-gray-600 my-8;
}

/* IMAGES */
.section-body :deep(img) {
  @apply my-6 rounded-xl max-w-full h-auto shadow-md;
}

/* TABLES (optionnel, si tu en prévois) */
.section-body :deep(table) {
  @apply w-full text-left border-collapse mb-6;
}
.section-body :deep(th),
.section-body :deep(td) {
  @apply border border-gray-300 dark:border-gray-700 px-4 py-2;
}
.section-body :deep(th) {
  @apply bg-gray-100 dark:bg-gray-700 font-semibold;
}
</style>


