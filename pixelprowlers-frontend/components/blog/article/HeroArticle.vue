<template>
  <section v-if="article" class="hero-article-container">
    <!-- Image -->
    <div class="hero-article-image-container">
      <img
        :src="article.image || 'https://placehold.co/600x400'"
        :alt="article.title"
        class="hero-article-image"
        loading="lazy"
      />
      <div class="hero-article-title-overlay-glass">
        <h1 class="hero-article-title">
          {{ article.title }}
        </h1>
      </div>
    </div>

    <!-- Infos -->
    <div class="hero-article-info">
      <p class="hero-article-date">
        {{ formatDate(article.created_at) }}
      </p>

      <div v-if="article.authors?.length" class="hero-article-author">
        <img
          :src="article.authors[0].avatar || '/images/default-avatar.png'"
          :alt="article.authors[0].name"
          class="hero-article-avatar"
        />
        <span class="hero-article-author-name">
          {{ article.authors[0].name }}
        </span>
      </div>

      <p class="hero-article-summary">
        {{ article.summary }}
      </p>

      <NuxtLink
        :to="`/blog/${article.slug}`"
        class="hero-article-button"
      >
        Lire l'article
      </NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{
  article: {
    title: string
    slug: string
    summary: string
    created_at: string
    image?: string | null
    authors?: { name: string; avatar?: string }[]
  }
}>()

const formatDate = (dateStr: string) => {
  const options: Intl.DateTimeFormatOptions = {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  }
  return new Date(dateStr).toLocaleDateString('fr-FR', options)
}
</script>

<style scoped>
@reference "@/assets/css/main.css";

.hero-article-container {
  @apply mt-12 flex flex-col lg:flex-row gap-6 mx-auto max-w-5xl bg-transparent border border-gray-700 rounded-2xl p-6 md:p-8 shadow-lg shadow-gray-700/30;
}

.hero-article-image-container {
  @apply relative w-full lg:w-5/12 rounded-xl overflow-hidden;
}

.hero-article-image {
  @apply w-full h-64 md:h-72 object-cover;
}

.hero-article-title-overlay-glass {
  @apply absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-md border border-white/20 shadow-md;
}

.hero-article-title {
  @apply text-4xl text-lg md:text-xl font-bold text-center;
}

.hero-article-info {
  @apply flex flex-col justify-between w-full lg:w-7/12 text-gray-100;
}

.hero-article-date {
  @apply text-sm text-gray-400 mb-2;
}

.hero-article-author {
  @apply flex items-center gap-2 mb-4;
}

.hero-article-avatar {
  @apply w-8 h-8 rounded-full object-cover border border-gray-600;
}

.hero-article-author-name {
  @apply text-sm font-medium text-gray-200;
}

.hero-article-summary {
  @apply text-base text-gray-300 mb-4 leading-relaxed;
}

.hero-article-button {
  @apply inline-block w-max px-4 py-2 bg-accent text-dark font-semibold rounded-md shadow hover:bg-accent/90 transition;
}
</style>

