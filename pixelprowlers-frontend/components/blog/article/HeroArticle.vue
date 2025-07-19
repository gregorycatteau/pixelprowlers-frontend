<template>
  <section v-if="article" class="hero-container">
    <!-- Image -->
    <div class="image-container">
      <img
        :src="article.image || 'https://placehold.co/600x400'"
        :alt="article.title"
        class="main-image"
        loading="lazy"
      />
      <div class="title-overlay">
        <h1 class="main-title">
          {{ article.title }}
        </h1>
      </div>
    </div>

    <!-- Infos -->
    <div class="info-container">
      <p class="article-date">
        {{ formatDate(article.created_at) }}
      </p>

      <div v-if="article.authors?.length" class="author-info">
        <img
          :src="article.authors[0].avatar || '/images/default-avatar.png'"
          :alt="article.authors[0].name"
          class="author-avatar"
        />
        <span class="author-name">
          {{ article.authors[0].name }}
        </span>
      </div>

      <p class="summary-text">
        {{ article.summary }}
      </p>

      <NuxtLink
        :to="`/blog/${article.slug}`"
        class="read-button"
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

.hero-container {
  @apply mt-12 flex flex-col lg:flex-row gap-6 mx-auto max-w-5xl bg-transparent border border-gray-700 rounded-2xl p-6 md:p-8 shadow-lg shadow-gray-700/30;
}

.image-container {
  @apply relative w-full lg:w-5/12 rounded-xl overflow-hidden;
}

.main-image {
  @apply w-full h-64 md:h-72 object-cover;
}

.title-overlay {
  @apply absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-md border border-white/20 shadow-md;
}

.main-title {
  @apply text-lg md:text-xl lg:text-4xl font-bold text-center;
}

.info-container {
  @apply flex flex-col justify-between w-full lg:w-7/12 text-gray-100;
}

.article-date {
  @apply text-sm text-gray-400 mb-2;
}

.author-info {
  @apply flex items-center gap-2 mb-4;
}

.author-avatar {
  @apply w-8 h-8 rounded-full object-cover border border-gray-600;
}

.author-name {
  @apply text-sm font-medium text-gray-200;
}

.summary-text {
  @apply text-base text-gray-300 mb-4 leading-relaxed;
}

.read-button {
  @apply inline-block w-max px-4 py-2 bg-accent text-dark font-semibold rounded-md shadow hover:bg-accent/90 transition;
}
</style>

