<template>
  <aside v-if="articles.length" class="related-articles-block">
    <h3 class="related-articles-title">Articles connexes</h3>
    <div class="related-articles-grid">
      <NuxtLink
        v-for="article in articles"
        :key="article.slug"
        :to="`/blog/${article.slug}`"
        class="related-article-card"
      >
        <img
          v-if="article.image"
          :src="article.image"
          :alt="article.title"
          class="related-article-image"
        />
        <div class="related-article-content">
          <h4 class="related-article-title">{{ article.title }}</h4>
          <p v-if="article.summary" class="related-article-summary">{{ article.summary }}</p>
        </div>
      </NuxtLink>
    </div>
  </aside>
</template>

<script setup lang="ts">
interface RelatedArticle {
  slug: string
  title: string
  summary?: string
  image?: string
}

defineProps<{ articles: RelatedArticle[] }>()
</script>

<style scoped>
@reference "@/assets/css/main.css";

.related-articles-block {
  @apply mt-20 px-4 md:px-0;
}

.related-articles-title {
  @apply text-2xl font-bold mb-6 text-neutral-900 dark:text-white;
}

.related-articles-grid {
  @apply grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6;
}

.related-article-card {
  @apply bg-white dark:bg-neutral-900 rounded-xl shadow hover:shadow-lg transition duration-300 overflow-hidden flex flex-col;
}

.related-article-image {
  @apply w-full h-40 object-cover;
}

.related-article-content {
  @apply p-4 flex-1 flex flex-col;
}

.related-article-title {
  @apply text-lg font-semibold text-neutral-900 dark:text-white;
}

.related-article-summary {
  @apply text-sm text-neutral-600 dark:text-neutral-400 mt-2 flex-grow;
}
</style>

