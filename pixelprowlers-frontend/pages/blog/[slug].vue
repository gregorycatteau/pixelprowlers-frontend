<template>
  <div
    v-if="article"
    class="article-layout-wrapper grid grid-cols-1 gap-8 max-w-7xl mx-auto px-4 pt-10 pb-20 lg:grid-cols-[280px_1fr_280px]"
  >
    <!-- ASIDE GAUCHE -->
    <aside class="article-sidebar-left hidden lg:block sticky top-20 self-start">

      <BlogFilter
        :articles="[article]"
        :categories="categoriesList"
        @update:category="onCategoryChange"
        @update:sort="onSortChange"
      />
    </aside>

    <!-- CONTENU CENTRAL -->
    <main class="article-content-wrapper">
      <section class="article-top-section">
        <img
          v-if="article.image"
          :src="article.image"
          alt="Image de couverture"
          class="article-cover-image"
        />

        <ArticleHeader
          v-if="article"
          class="article-header-card"
          :title="article.title"
          :date="formatDate(article.created_at)"
          :category="article.category.name"
          :authors="article.authors"
        />
      </section>

      <section
        class="article-sections-container"
        v-if="article.sections"
      >
        <SectionBlock
          v-for="section in article.sections"
          :key="section.order"
          :id="`section-${section.order}`"
          :title="section.title"
          :content="section.content"
          :image="section.image"
        />

        <Footnotes
          class="article-footnotes"
          :notes="article.footnotes || []"
        />
        <RelatedArticles
          class="article-related-articles"
          :articles="article.related_articles || []"
        />
      </section>
    </main>

    <!-- ASIDE DROIT -->
    <aside class="article-sidebar-right hidden lg:block sticky top-20 self-start">
      <TableOfContents :items="tocItems" />
    </aside>
  </div>

  <p v-else class="article-error-message">
    Article introuvable ou en cours de chargement...
  </p>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'blog',
})

import { ref, watch, computed } from 'vue'
import { useRoute, useRuntimeConfig, useFetch } from 'nuxt/app'
import DOMPurify from 'dompurify'

import ArticleHeader from '@/components/blog/article/ArticleHeader.vue'
import SectionBlock from '@/components/blog/article/SectionBlock.vue'
import Footnotes from '@/components/blog/article/FootNotes.vue'
import RelatedArticles from '@/components/blog/article/RelatedArticles.vue'
import TableOfContents from '@/components/blog/article/TableOfContents.vue'
import BlogFilter from '@/components/blog/BlogFilters.vue'

interface Author {
  name: string
  role?: string
  avatar?: string
}

interface Section {
  title: string
  content: string
  image?: string
  order: number
}

interface Footnote {
  text: string
  order: number
}

interface Article {
  id: number
  title: string
  slug: string
  summary: string
  content: string
  created_at: string
  image?: string
  category: {
    id: number
    name: string
    slug: string
  }
  authors?: Author[]
  sections?: Section[]
  footnotes?: Footnote[]
  related_articles?: any[]
}

interface Category {
  id: number
  name: string
  slug: string
}

const route = useRoute()
const slug = ref(route.params.slug as string)

const runtimeConfig = useRuntimeConfig()

const { data: article, pending, refresh } = useFetch<Article>(
  `/blog/articles/${slug.value}/`,
  {
    baseURL: runtimeConfig.public.apiBaseUrl,
    key: `article-${slug.value}`,
    server: false,
    watch: [slug],
  }
)

const { data: categories } = useFetch<Category[]>(
  '/blog/categories/',
  {
    baseURL: runtimeConfig.public.apiBaseUrl,
    key: 'categories',
    server: false,
  }
)

const categoriesList = computed(() =>
  categories.value ? categories.value.map((c) => c.name) : []
)

watch(
  () => route.params.slug,
  (newSlug) => {
    slug.value = newSlug as string
    refresh()
  }
)

const tocItems = computed(() =>
  (article.value?.sections || []).map((s) => ({
    id: `section-${s.order}`,
    title: DOMPurify.sanitize(s.title),
  }))
)

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

function onCategoryChange(newCategory: string) {
  console.log('Catégorie sélectionnée :', newCategory)
}

function onSortChange(newSort: string) {
  console.log('Tri sélectionné :', newSort)
}
</script>

<style scoped>
@reference "@/assets/css/main.css";
.article-layout-wrapper {
  @apply grid grid-cols-1 lg:grid-cols-[280px_1fr_280px] gap-8 max-w-7xl mx-auto px-4 pt-10 pb-20;
}

.article-sidebar-left {
  @apply hidden lg:block;
}

.article-sidebar-right {
  @apply hidden lg:block sticky top-20 self-start;
}

.article-content-wrapper {
  @apply space-y-16;
}

.article-top-section {
  @apply space-y-8;
}

.article-cover-image {
  @apply w-full rounded-xl shadow-lg max-h-[28rem] object-cover;
}

.article-header-card {
  @apply bg-gray-900 text-white rounded-xl p-6 shadow-md space-y-2;
}

.article-sections-container {
  @apply space-y-16 text-lg leading-relaxed text-gray-200;
}

.article-footnotes {
  @apply text-sm text-gray-400 border-t border-gray-700 pt-6 mt-12;
}

.article-related-articles {
  @apply mt-20 pt-10 border-t border-gray-700;
}

.article-error-message {
  @apply text-center py-12 text-red-500 text-lg;
}
</style>
