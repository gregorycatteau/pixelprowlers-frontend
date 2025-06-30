<template>
  <header class="header-container">
    <h1 class="header-title">{{ title }}</h1>
    <p class="header-meta">
      <span>{{ date }}</span>
      <span v-if="category"> • {{ category }}</span>
    </p>

    <div v-if="authors?.length" class="authors-container">
      <div
        v-for="author in authors"
        :key="author.name"
        class="author-card"
      >
        <img
          v-if="author.avatar"
          :src="author.avatar"
          :alt="author.name"
          class="author-avatar"
        />
        <div>
          <p class="author-name">{{ author.name }}</p>
          <p v-if="author.role" class="author-role">{{ author.role }}</p>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
export interface Author {
  name: string
  role?: string
  avatar?: string
}

defineProps<{ title: string; date: string; category?: string; authors?: Author[] }>()
</script>

<style scoped>
@reference "@/assets/css/main.css";

.header-container {
  @apply space-y-4 mb-10;
}

.header-title {
  @apply text-3xl md:text-4xl font-extrabold tracking-tight leading-tight text-gray-900 dark:text-accent;
}

.header-meta {
  @apply text-gray-500 text-base md:text-lg;
}

.authors-container {
  @apply flex flex-wrap gap-4 mt-4;
}

.author-card {
  @apply flex items-center space-x-3 bg-gray-100 dark:bg-neutral-800 rounded-lg px-3 py-2 shadow transition hover:shadow-md;
}

.author-avatar {
  @apply w-10 h-10 rounded-full object-cover;
}

.author-name {
  @apply font-medium text-gray-900 dark:text-white;
}

.author-role {
  @apply text-xs text-gray-500 dark:text-gray-400;
}
</style>

