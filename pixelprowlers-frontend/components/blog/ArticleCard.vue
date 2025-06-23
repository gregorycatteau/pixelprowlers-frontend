<template>
  <div v-if="pending" class="text-center py-6">Chargement...</div>
  <article v-else class="article-wrapper">
    <section class="cover-image">
      <img
        :src="article.image || 'https://placehold.co/1200x600'"
        :alt="article.title"
        class="cover-img"
      />
    </section>

    <section class="body-section">
      <NuxtLink to="/blog" class="back-btn">
        &larr; Tous les articles
      </NuxtLink>
      <h1 class="article-title">{{ article.title }}</h1>
      <p class="meta">
        {{ new Date(article.created_at).toLocaleDateString() }}
        • {{ article.category.name }}
      </p>
      <div class="article-content" v-html="article.content" />
    </section>
  </article>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const route = useRoute()
const slug = ref(route.params.slug as string)
const article = ref<any>({})
const pending = ref(true)

async function fetchArticle(slugValue: string) {
  pending.value = true
  try {
    const { data } = await useFetch(`/api/blog/articles/${slugValue}`, {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
    })
    article.value = data.value || {}
  } catch (error) {
    article.value = {}
  } finally {
    pending.value = false
  }
}

watch(() => route.params.slug, async (newSlug) => {
  slug.value = newSlug as string
  await fetchArticle(slug.value)
})

onMounted(async () => {
  await fetchArticle(slug.value)
})
</script>

<style scoped>
@reference "@/assets/css/main.css";
.article-wrapper {
  @apply bg-transparent dark:text-primary flex flex-col min-h-screen;
}
.cover-image {
  @apply w-full h-72 md:h-[60vh] overflow-hidden;
}
.cover-img {
  @apply w-full h-full object-cover;
}
.body-section {
  @apply mx-auto px-4 py-8 md:py-12 w-full max-w-3xl space-y-6;
}
.article-title {
  @apply font-display text-4xl md:text-5xl font-bold;
}
.meta {
  @apply text-sm text-gray-400 mb-4;
}
.article-content {
  @apply max-w-[65ch] leading-relaxed space-y-6;
}
.back-btn {
  @apply text-accent mb-6 inline-block transition-transform;
}
</style>

