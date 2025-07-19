<template>
  <div class="blog-filter-container">
    <!-- Bandeau principal -->
    <div class="blog-header">
      <h2 class="blog-title">Le meilleur du blog Pixelprowlers</h2>
      <button @click="onSubscribeClick" class="subscribe-button">Je m'inscris</button>
    </div>

    <!-- Bandeau filtres -->
    <div class="filter-bar">
      <!-- Menu catégories -->
      <select v-model="localCategory" @change="emitCategory" class="category-select">
        <option value="">Toutes les catégories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>

      <!-- Icônes filtres -->
      <div class="filter-icons">
        <button @click="toggleSortMenu" type="button" class="sort-icon-button">
          <svg xmlns="http://www.w3.org/2000/svg" class="sort-icon-svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0-4a1 1 0 011-1h8a1 1 0 110 2H4a1 1 0 01-1-1zm0 8a1 1 0 011-1h4a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
          </svg>
        </button>

        <select v-model="localSortType" @change="emitSortType" class="sort-select">
          <option value="date">Date</option>
          <option value="popular">Popularité</option>
        </select>
      </div>
    </div>

    <!-- Liste articles -->
    <ul class="article-list">
      <li v-for="article in displayedArticles" :key="article.id" class="article-item">
        <a :href="`/blog/${article.slug}`" class="article-link">{{ article.title }}</a>
        <span class="article-date">{{ formatDate(article.created_at) }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { Article } from '@/composables/useArticles'

const props = defineProps<{
  articles: Article[]
  categories: string[]
}>()

const emit = defineEmits(['update:category', 'update:sort'])

const localCategory = ref('')
const localSortType = ref<'date' | 'popular'>('date')

function emitCategory() {
  emit('update:category', localCategory.value)
}

function emitSortType() {
  emit('update:sort', localSortType.value)
}

function onSubscribeClick() {
  console.log('Clicked subscribe!')
}

const displayedArticles = computed(() => {
  let filtered = props.articles

  if (localCategory.value) {
    filtered = filtered.filter((a) =>
      typeof a.category === 'string'
        ? a.category === localCategory.value
        : a.category.name === localCategory.value
    )
  }

  if (localSortType.value === 'date') {
    filtered = filtered.sort(
      (a, b) => Number(new Date(b.created_at)) - Number(new Date(a.created_at))
    )
  }

  return filtered
})

function toggleSortMenu() {
  console.log('Toggle sort menu clicked')
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>

<style scoped>
@reference "@/assets/css/main.css";
.blog-filter-container {
  @apply bg-gray-900/95 text-white p-6 rounded-2xl border border-gray-800 shadow-xl space-y-6 min-w-[260px];
}

.blog-header {
  @apply flex flex-col items-start space-y-3;
}

.blog-title {
  @apply text-base font-bold leading-tight;
}

.subscribe-button {
  @apply self-stretch bg-accent text-white font-semibold text-sm px-4 py-2 rounded-lg hover:bg-accent/90 transition text-center;
}

.filter-bar {
  @apply space-y-4;
}

.category-select,
.sort-select {
  @apply w-full bg-gray-800 border border-gray-700 text-white rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-accent;
}

.filter-icons {
  @apply flex flex-row justify-between items-center;
}

.sort-icon-button {
  @apply p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition;
}

.sort-icon-svg {
  @apply h-5 w-5 text-gray-400;
}

.article-list {
  @apply space-y-3 border-t border-gray-700 pt-4;
}

.article-item {
  @apply flex flex-col px-3 py-2 rounded-lg hover:bg-gray-800 transition;
}

.article-link {
  @apply text-accent font-medium text-sm hover:underline;
}

.article-date {
  @apply text-xs text-gray-400 mt-0.5;
}

</style>
